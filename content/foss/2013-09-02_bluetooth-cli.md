Title: Quick ObexPUSH Command
Category: foss
Tags: bluetooth, Arch Linux, cli, shell
Summary: Quick ObexPUSH File Send from Your Shell

# Quick ObexPUSH Command

Say you've got a file, `shoppinglist.txt`, that you want to send to your phone. And, you do not have BlueDevil, BlueMan or another GUI installed. With [Arch Linux](https://www.archlinux.org/‎) `bluez` and `obexftp`, it is super easy:

    :::sh
    obexftp \
        -v \
        -U none \
        -H \
        -S \
        -T30 \
        -b XX:XX:XX:XX:XX:XX \
        --channel $(sdptool browse | \
                    grep -A5 '0x1105' | \
                    grep Channel | \
                    cut -d':' -f2) \
        -p <path>/<file>;

That's all folks.
