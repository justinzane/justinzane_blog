Title: Arch + Grub2 + RackSpace = Trouble
Category: foss
Tags: Arch Linux, Grub, RackSpace, OpenStack
Summary: Fixing Arch Linux' Grub to work on RackSpace

# Arch + Grub2 + RackSpace = Trouble

I recently had a very annoying experience with one of my RackSpace cloud servers. It was running 
Arch and I installed a few upgrades -- `pacman -Syu` -- which included a kernel upgade. In the 
process of the upgrade, everything worked exactly as any Arch user would expect. `mkinitcpio` 
built an initramfs image and `grub-mkconfig` built a `/boot/grub/grub.cfg` file.

To me, that seemed spiffy... So I simply typed `shutdown -r -t 0 now` over ssh, waited a 
minute, and tried to login again. **Doh!!!** No ssh, no ping and a big <style="color: #ff0000;">
ERROR</style> on the RackSpace web console.

After going through several cycles of RS' "Chat" support where they would "activate" the server 
for me so that I could put it into "rescue" mode but were unable to provide specifics on what I 
needed to fix; one of them had the sense to mention that I could access the error messages 
directly using the API.

*Aside: The Arch AUR packages for pyrax are currently in a very bad state. Try to avoid them.*

I ran `sudo pip2 install pyrax` and was able to quickly and easily access the RackSpace cloud 
from within iPython2. I'll skip the details on that since both the pyrax and RackSpace docs are 
quite good for the basics.

I also quickly learned that the error message provided is rather limited in specificity:

    srv.fault
    Out[11]: 
    {u'code': 500,
     u'created': u'2015-02-14T10:49:19Z',
     u'message': u'["Using <class \'grub.GrubConf.Grub2ConfigFile\'> to parse /boot/grub/grub.cfg", 
                    \'Traceback (most recent call last):\', 
                    \'  File "/usr/bin/pygrub", line 850, in ?\', 
                    \'    raise RuntimeError, "Unable to find partition containing kernel"\', 
                    \'RuntimeError: Unable '
    }

I spent the better part of a day on IRC (`#rackspace`), the RackSpace, Arch and OpenStack wikis 
as well as whatever Google suggested. There was little real information about the exact situation 
but I did discover that PyGrub seems unable to use UUIDs. So, using the grub2 online manual as a
basis, stipped and modified the autogenerated grub.cfg into one that worked.

## The Working Version

    # WORKING /etc/grub/grub.cfg
    ### BEGIN /etc/grub.d/00_header ###
    insmod part_gpt
    insmod part_msdos
    insmod ext2
    insmod gzio
    insmod xzio
    insmod all_video
    insmod efi_gop
    insmod efi_uga
    insmod ieee1275_fb
    insmod vbe
    insmod vga
    insmod video_bochs
    insmod video_cirrus
    set timeout=5

    ### BEGIN /etc/grub.d/10_linux ###
    menuentry 'Arch Linux xvda1' {
        insmod gzio
        insmod xzio
        insmod part_msdos 
        insmod ext2
        search --no-floppy --fs-uuid --set=root bdeb55be-eeb4-42f9-83dd-2d11ecefd883 --hint hd0,msdos1
        linux  /boot/vmlinuz-linux root=/dev/xvda1 rw zswap.enabled=1 console=hvc0 
        initrd /boot/initramfs-linux.img
    }
    menuentry 'Arch Linux xvdb1' {
        insmod gzio
        insmod xzio
        insmod part_msdos 
        insmod ext2
        search --no-floppy --fs-uuid --set=root bdeb55be-eeb4-42f9-83dd-2d11ecefd883 --hint hd1,msdos1
        linux  /boot/vmlinuz-linux root=/dev/xvdb1 rw zswap.enabled=1 console=hvc0 
        initrd /boot/initramfs-linux.img
    }
    ### END /etc/grub.d/10_linux ###

## The Broken-on-RackSpace Version

    # DOES NOT WORK WITH PYGRUB
    #
    # DO NOT EDIT THIS FILE
    #
    # It is automatically generated by grub-mkconfig using templates
    # from /etc/grub.d and settings from /etc/default/grub
    #

    ### BEGIN /etc/grub.d/00_header ###
    insmod part_gpt
    insmod part_msdos
    if [ -s $prefix/grubenv ]; then
    load_env
    fi
    if [ "${next_entry}" ] ; then
    set default="${next_entry}"
    set next_entry=
    save_env next_entry
    set boot_once=true
    else
    set default="0"
    fi

    if [ x"${feature_menuentry_id}" = xy ]; then
    menuentry_id_option="--id"
    else
    menuentry_id_option=""
    fi

    export menuentry_id_option

    if [ "${prev_saved_entry}" ]; then
    set saved_entry="${prev_saved_entry}"
    save_env saved_entry
    set prev_saved_entry=
    save_env prev_saved_entry
    set boot_once=true
    fi

    function savedefault {
    if [ -z "${boot_once}" ]; then
        saved_entry="${chosen}"
        save_env saved_entry
    fi
    }

    function load_video {
    if [ x$feature_all_video_module = xy ]; then
        insmod all_video
    else
        insmod efi_gop
        insmod efi_uga
        insmod ieee1275_fb
        insmod vbe
        insmod vga
        insmod video_bochs
        insmod video_cirrus
    fi
    }

    if [ x$feature_default_font_path = xy ] ; then
    font=unicode
    else
    insmod part_msdos 
    insmod ext2
    if [ x$feature_platform_search_hint = xy ]; then
    search --no-floppy --fs-uuid --set=root  bdeb55be-eeb4-42f9-83dd-2d11ecefd883
    else
    search --no-floppy --fs-uuid --set=root bdeb55be-eeb4-42f9-83dd-2d11ecefd883
    fi
        font="/usr/share/grub/unicode.pf2"
    fi

    if loadfont $font ; then
    set gfxmode=auto
    load_video
    insmod gfxterm
    fi
    terminal_output gfxterm
    if [ x$feature_timeout_style = xy ] ; then
    set timeout_style=menu
    set timeout=5
    # Fallback normal timeout code in case the timeout_style feature is
    # unavailable.
    else
    set timeout=5
    fi
    ### END /etc/grub.d/00_header ###

    ### BEGIN /etc/grub.d/10_linux ###
    menuentry 'Arch Linux' --class arch --class gnu-linux --class gnu --class os $menuentry_id_option 'gnulinux-simple-bdeb55be-eeb4-42f9-83dd-2d11ecefd883' {
        load_video
        insmod gzio
        insmod part_msdos 
        insmod ext2
        if [ x$feature_platform_search_hint = xy ]; then
        search --no-floppy --fs-uuid --set=root  bdeb55be-eeb4-42f9-83dd-2d11ecefd883
        else
        search --no-floppy --fs-uuid --set=root bdeb55be-eeb4-42f9-83dd-2d11ecefd883
        fi
        echo	'Loading Linux linux ...'
        linux	/boot/vmlinuz-linux root=/dev/xvda1 rw zswap.enabled=1 console=hvc0 
        echo	'Loading initial ramdisk ...'
        initrd	 /boot/initramfs-linux.img
    }
    submenu 'Advanced options for Arch Linux' $menuentry_id_option 'gnulinux-advanced-bdeb55be-eeb4-42f9-83dd-2d11ecefd883' {
        menuentry 'Arch Linux, with Linux linux' --class arch --class gnu-linux --class gnu --class os $menuentry_id_option 'gnulinux-linux-advanced-bdeb55be-eeb4-42f9-83dd-2d11ecefd883' {
            load_video
            insmod gzio
            insmod part_msdos 
            insmod ext2
            if [ x$feature_platform_search_hint = xy ]; then
            search --no-floppy --fs-uuid --set=root  bdeb55be-eeb4-42f9-83dd-2d11ecefd883
            else
            search --no-floppy --fs-uuid --set=root bdeb55be-eeb4-42f9-83dd-2d11ecefd883
            fi
            echo	'Loading Linux linux ...'
            linux	/boot/vmlinuz-linux root=/dev/xvda1 rw zswap.enabled=1 console=hvc0 
            echo	'Loading initial ramdisk ...'
            initrd	 /boot/initramfs-linux.img
        }
    }

    ### END /etc/grub.d/10_linux ###

    ### BEGIN /etc/grub.d/20_linux_xen ###
    ### END /etc/grub.d/20_linux_xen ###

    ### BEGIN /etc/grub.d/30_os-prober ###
    ### END /etc/grub.d/30_os-prober ###

    ### BEGIN /etc/grub.d/40_custom ###
    # This file provides an easy way to add custom menu entries.  Simply type the
    # menu entries you want to add after this comment.  Be careful not to change
    # the 'exec tail' line above.
    ### END /etc/grub.d/40_custom ###

    ### BEGIN /etc/grub.d/41_custom ###
    if [ -f  ${config_directory}/custom.cfg ]; then
    source ${config_directory}/custom.cfg
    elif [ -z "${config_directory}" -a -f  $prefix/custom.cfg ]; then
    source $prefix/custom.cfg;
    fi
    ### END /etc/grub.d/41_custom ###

    ### BEGIN /etc/grub.d/60_memtest86+ ###
    ### END /etc/grub.d/60_memtest86+ ###

## TODO

While I've got a server that is back and running, this is not a real fix. The next step is to 
work to develop a set of scripts (`/etc/grub.d/*`) and a config (`/etc/default/grub`) and 
package them so that they reliably replace the standard Arch setup for OpenStack / RackSpace 
hosts.
