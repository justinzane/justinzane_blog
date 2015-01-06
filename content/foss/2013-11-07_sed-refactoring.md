Title: Refactoring with Sed
Category: foss
Tags: refactoring, c, c++, sed
Summary: Refactoring c/c++ includes with sed.

# Refactoring c/c++ includes with sed.

Since c++ is one of the most complex and "expert friendly" languages around, there are fewer 
tools for automated refactoring of c++ source than there are for other, more structured and 
limited languages. While that seems like a problem, it really is not.

The basic GNU / *nix utilities like cat, grep, sed, tr, cut, wc and friends have been around 
since the 1970s. The were written by the fathers of Unix and of system programming languages 
like c and c++ for use programming Unix systems. So, the are excellent, if thoroughly 
underappreciated tools for the job.

I'm trying to refactor a reasonably large project by moving related source files into logical 
directories. This has been partially done already, so refactoring is more complicated than: 
`sed -i 's|#include "bar.hpp"|#include "foo/bar.hpp"'`. There are likely to be instances of 
`"../bar.hpp"`, `<bar.hpp>`, `../../../../bar.hpp`, etc. 

The solution to moving `./unit*.hpp` files to `./unit/` is:

    :::sh
    for i in $(grep --include="*.cpp" --include="*.hpp" --include="*.c" --include="*.h" -rl '#include'); do 
        sed -i -r '\|#include.+[<"](\.\./)*unit[_a-z]*\.h| s|(unit[_a-z]*\.h)|unit/&|' $i; 
    done
    
The first part of the sed command only matches the lines we care about. The second replaces the 
part we care about without touching the rest.
