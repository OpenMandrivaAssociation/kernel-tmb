#
# *tmb* series kernels now use kernel.org versioning
#
%define kernelversion	2
%define patchlevel	6
%define sublevel	20

# kernel Makefile extraversion is substituted by 
# kpatch/kstable wich are either 0 (empty), pre/rc (kpatch) or stable release (kstable)
%define kpatch		0
%define kstable		4

# this is the releaseversion
%define kbuild		4

%define ktag 		tmb
%define kname 		kernel-%{ktag}

%define rpmtag		%distsuffix
%if %kpatch
%define rpmrel		%mkrel 0.%{kpatch}.%{kbuild}
%else
%define rpmrel		%mkrel %{kbuild}
%endif

# theese two never change, they are used to fool rpm/urpmi/smart
%define fakever		1
%define fakerel		%mkrel 1

# When we are using a pre/rc patch, the tarball is a sublevel -1
%if %kpatch
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}
%define tar_ver	  	%{kernelversion}.%{patchlevel}.%(expr %{sublevel} - 1)
%else
%if %kstable
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}.%{kstable}
%define tar_ver   	%{kernelversion}.%{patchlevel}.%{sublevel}
%else
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}
%define tar_ver   	%{kversion}
%endif
%endif
%define patch_ver 	%{kversion}-%{ktag}%{kbuild}
%define kverrel   	%{kversion}-%{rpmrel}

# used for not making too long names for rpms or search paths 
%if %kpatch
%define buildrpmrel     0.%{kpatch}.%{kbuild}%{rpmtag}
%else
%define buildrpmrel     %{kbuild}%{rpmtag}
%endif
%define buildrel     	%{kversion}-%{buildrpmrel}

# having different top level names for packges means that you have to remove them by hard :(
%define top_dir_name 	%{kname}-%{_arch}

%define build_dir 	${RPM_BUILD_DIR}/%{top_dir_name}
%define src_dir 	%{build_dir}/linux-%{tar_ver}

# disable useless debug rpms...
%define _enable_debug_packages 	%{nil}
%define debug_package 		%{nil}

# Build defines
%define build_doc 		0
%define build_source 		1
%define build_devel 		1
%define build_debug 		0

# Build desktop i586 / 1GB
%ifarch %{ix86}
%define build_desktop586_up  	1
%define build_desktop586_smp 	1
%endif

# Build mm (i686 / 4GB) / x86_64 / sparc64 sets
%define build_desktop_up  	1
%define build_desktop_smp 	1

# Build laptop (i686 / 4GB)/ x86_64 / sparc64 sets
%define build_laptop_up  	0
%define build_laptop_smp 	0

# Build server (i686 / 64GB)/x86_64 / sparc64 sets
%define build_server_up  	1
%define build_server_smp 	1

# End of user definitions
%{?_without_desktop586_up: %global build_desktop586_up 0}
%{?_without_desktop586_smp: %global build_desktop586_smp 0}
%{?_without_desktop_up: %global build_desktop_up 0}
%{?_without_desktop_smp: %global build_desktop_smp 0}
%{?_without_laptop_up: %global build_laptop_up 0}
%{?_without_laptop_smp: %global build_laptop_smp 0}
%{?_without_server_up: %global build_server_up 0}
%{?_without_server_smp: %global build_server_smp 0}
%{?_without_doc: %global build_doc 0}
%{?_without_source: %global build_source 0}
%{?_without_devel: %global build_devel 0}
%{?_without_debug: %global build_debug 0}

%{?_with_desktop586_up: %global build_desktop586_up 1}
%{?_with_desktop586_smp: %global build_desktop586_smp 1}
%{?_with_desktop_up: %global build_desktop_up 1}
%{?_with_desktop_smp: %global build_desktop_smp 1}
%{?_with_laptop_up: %global build_laptop_up 1}
%{?_with_laptop_smp: %global build_laptop_smp 1}
%{?_with_server_up: %global build_server_up 1}
%{?_with_server_smp: %global build_server_smp 1}
%{?_with_doc: %global build_doc 1}
%{?_with_source: %global build_source 1}
%{?_with_devel: %global build_devel 1}
%{?_with_debug: %global build_debug 1}

# For the .nosrc.rpm
%define build_nosrc 	0
%{?_with_nosrc: %global build_nosrc 1}

%define kmake %make
# there are places where parallel make don't work
%define smake make

# Sparc arch wants sparc64 kernels
%define target_arch    %(echo %{_arch} | sed -e "s/sparc/sparc64/")

#
# SRC RPM description
#
Summary: 	Linux kernel built for Mandriva with modifications by %{ktag}
Name:		%{kname}
Version: 	%{kversion}
Release: 	%{rpmrel}
License: 	GPL
Group: 	 	System/Kernel and hardware
ExclusiveArch: 	%{ix86} x86_64 sparc64
ExclusiveOS: 	Linux
URL: 		http://www.kernel.org/

####################################################################
#
# Sources
#
### This is for full SRC RPM
Source0: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.bz2
Source1: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.bz2.sign
### This is for stripped SRC RPM
%if %build_nosrc
NoSource: 0
%endif

Source4: 	README.kernel-%{ktag}-sources
Source5: 	README.Mandriva_Linux_%{ktag}
Source6: 	README.%{ktag}.urpmi

Source100: 	linux-%{patch_ver}.tar.bz2
Source101: 	linux-%{patch_ver}.tar.bz2.sign
Source102: 	%{kname}.patchlist

####################################################################
#
# Patches

#
# Patch0 to Patch100 are for core kernel upgrades.
#

# Pre linus patch: ftp://ftp.kernel.org/pub/linux/kernel/v2.6/testing

%if %kpatch
Patch1:		ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}
Source10: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}.bz2.sign
%endif
%if %kstable
Patch1:   	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/patch-%{kversion}
Source10: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/patch-%{kversion}.bz2.sign
%endif

#END
####################################################################

# Defines for the things that are needed for all the kernels
#
%define kinfo1 	The kernel package contains the Linux kernel (vmlinuz), the core of your
%define kinfo2 	Mandriva Linux operating system.  The kernel handles the basic functions
%define kinfo3 	of the operating system:  memory allocation, process allocation, device

%define upinfo1	For instructions for update, see:
%define upinfo2	http://www.mandriva.com/security/kernelupdate

%define info1 	The %{ktag} kernels is an experimental kernel based on the kernel.org 
%define info2 	kernels with added patches. Some of them may/will never end up in
%define info3 	the main kernels due to their experimental nature. Some refer to
%define info4 	this kernel as a 'hackkernel' ...
%define info5 	Use these kernels at your own risk !!

%define info10 	If you want more info on the various %{kname} flavours, please visit:
%define info11 	http://www.iki.fi/tmb/Kernels/
 
### Global Requires/Provides
%define requires1 	mkinitrd >= 4.2.17-%mkrel 20
%define requires2 	bootloader-utils >= 1.12-%mkrel 1
%define requires3 	sysfsutils >= 1.3.0-%mkrel 1 module-init-tools >= 3.2-0.pre8.%mkrel 2

%define kprovides 	%{kname} = %{kverrel}, kernel = %{tar_ver}

BuildRoot: 		%{_tmppath}/%{kname}-%{kversion}-build
Autoreqprov: 		no
Requires(pre): 		%requires1
Requires(pre): 		%requires2
Requires(pre): 		%requires3
BuildRequires: 		gcc >= 4.0.1-%mkrel 5 module-init-tools >= 3.2-0.pre8.%mkrel 2

%description
%{kinfo1}
%{kinfo2}
%{kinfo3}
input and output, etc.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-desktop586: i586, up, 1GB
#

%package -n %{kname}-desktop586-%{buildrel}
Version: 	%{fakever}
Release: 	%{fakerel}
Provides: 	%kprovides
Requires(pre): 	%requires1
Requires(pre): 	%requires2
Requires(pre): 	%requires3
Summary: 	Linux kernel for desktop use with i586-up-1GB 
Group: 		System/Kernel and hardware

%description -n %{kname}-desktop586-%{buildrel}
%{kinfo1}
%{kinfo2}
%{kinfo3}
input and output, etc. This kernel is compiled for desktop use, single
i586 processor/core and less than 1GB RAM (usually 870-900MB detected),
using voluntary preempt and cfq scheduler.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-desktop586-smp: i586, smp, 1GB
#

%package -n %{kname}-desktop586-smp-%{buildrel}
Version: 	%{fakever}
Release: 	%{fakerel}
Provides: 	%kprovides
Requires(pre): 	%requires1
Requires(pre): 	%requires2
Requires(pre): 	%requires3
Summary: 	Linux kernel for desktop use with i586-smp-1GB 
Group: 		System/Kernel and hardware

%description -n %{kname}-desktop586-smp-%{buildrel}
%{kinfo1}
%{kinfo2}
%{kinfo3}
input and output, etc. This kernel is compiled for desktop use, multiple
i586 processors/cores and less than 1GB RAM (usually 870-900MB detected),
using voluntary preempt and cfq scheduler.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-desktop: i686, up, 4 GB / x86_64
#
%package -n %{kname}-desktop-%{buildrel}
Version: 	%{fakever}
Release: 	%{fakerel}
Provides: 	%kprovides
Requires(pre): 	%requires1
Requires(pre): 	%requires2
Requires(pre): 	%requires3
%ifarch %{ix86}
Summary: 	Linux Kernel for desktop use with i686-up-4GB
%else
Summary: 	Linux Kernel for desktop use with x86_64-up
%endif
Group: 		System/Kernel and hardware

%ifarch %{ix86}
%description -n %{kname}-desktop-%{buildrel}
%{kinfo1}
%{kinfo2}
%{kinfo3}
input and output, etc. This kernel is compiled for desktop use, single
i686 processor/core and less than 4GB RAM, using voluntary preempt and 
cfq scheduler.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}
%else
%description -n %{kname}-desktop-%{buildrel}
%{kinfo1}
%{kinfo2}
%{kinfo3}
input and output, etc. This kernel is compiled for desktop use, single
x86_64 processor/core, using voluntary preempt and cfq scheduler.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}
%endif



#
# kernel-tmb-desktop-smp: i686, smp, 4 GB / x86_64
#
%package -n %{kname}-desktop-smp-%{buildrel}
Version: 	%{fakever}
Release: 	%{fakerel}
Provides: 	%kprovides
Requires(pre): 	%requires1
Requires(pre): 	%requires2
Requires(pre): 	%requires3
%ifarch %{ix86}
Summary: 	Linux Kernel for desktop use with i686-smp-4GB
%else
Summary: 	Linux Kernel for desktop use with x86_64-smp
%endif
Group: 		System/Kernel and hardware

%ifarch %{ix86}
%description -n %{kname}-desktop-smp-%{buildrel}
%{kinfo1}
%{kinfo2}
%{kinfo3}
input and output, etc. This kernel is compiled for desktop use, multiple
i686 processors/cores and less than 4GB RAM, using voluntary preempt and 
cfq scheduler.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}
%else
%description -n %{kname}-desktop-smp-%{buildrel}
%{kinfo1}
%{kinfo2}
%{kinfo3}
input and output, etc. This kernel is compiled for desktop use, multiple
x86_64 processors/cores, using voluntary preempt and cfq scheduler.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}
%endif



#
# kernel-tmb-laptop: i686, up, 4GB / x86_64
#
%package -n %{kname}-laptop-%{buildrel}
Version: 	%{fakever}
Release: 	%{fakerel}
Provides: 	%kprovides
Requires(pre): 	%requires1
Requires(pre): 	%requires2
Requires(pre): 	%requires3
%ifarch %{ix86}
Summary: 	Linux kernel for laptop use with i686-up-4GB 
%else
Summary: 	Linux kernel for laptop use with x86_64
%endif
Group: 		System/Kernel and hardware

%ifarch %{ix86}
%description -n %{kname}-laptop-%{buildrel}
%{kinfo1}
%{kinfo2}
%{kinfo3}
input and output, etc. This kernel is compiled for laptop use, single
i686 processor/core and less than 4GB RAM, using HZ_100 to save battery,
voluntary preempt and cfq scheduler, and some other laptop-specific
optimizations. If you want to sacrifice battery life for performance,
you better use the %{kname}-desktop686.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}
%else
%description -n %{kname}-laptop-%{buildrel}
%{kinfo1}
%{kinfo2}
%{kinfo3}
input and output, etc. This kernel is compiled for laptop use, single
x86_64 processor/core, using HZ_100 to save battery, voluntary preempt 
and cfq scheduler, and some other laptop-specific optimizations. If you 
want to sacrifice battery life for performance, you better use the 
%{kname}-desktop.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}
%endif



#
# kernel-laptop-smp: i686, smp, 4GB / x86_64
#
%package -n %{kname}-laptop-smp-%{buildrel}
Version: 	%{fakever}
Release: 	%{fakerel}
Provides: 	%kprovides
Requires(pre): 	%requires1
Requires(pre): 	%requires2
Requires(pre): 	%requires3
%ifarch{ix86}
Summary: 	Linux kernel for laptop use with i686-smp-4GB 
%else
Summary: 	Linux kernel for laptop use with x86_64-smp
%endif 
Group: 		System/Kernel and hardware

%ifarch{ix86}
%description -n %{kname}-laptop-smp-%{buildrel}
%{kinfo1}
%{kinfo2}
%{kinfo3}
input and output, etc. This kernel is compiled for laptop use, multiple
i686 processors/cores and less than 4GB RAM, using HZ_100 to save battery,
voluntary preempt and cfq scheduler, and some other laptop-specific
optimizations. If you want to sacrifice battery life for performance,
you better use the %{kname}-desktop686-smp.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}
%else
%description -n %{kname}-laptop-smp-%{buildrel}
%{kinfo1}
%{kinfo2}
%{kinfo3}
input and output, etc. This kernel is compiled for desktop use, multiple
x86_64 processors/cores, using HZ_100 to save battery, voluntary preempt 
and cfq scheduler, and some other laptop-specific optimizations. If you 
want to sacrifice battery life for performance, you better use the 
%{kname}-desktop-smp.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}
%endif



#
# kernel-tmb-server: i686, up, 64 GB /x86_64
#
%package -n %{kname}-server-%{buildrel}
Version: 	%{fakever}
Release: 	%{fakerel}
Provides: 	%kprovides
Requires(pre): 	%requires1
Requires(pre): 	%requires2
Requires(pre): 	%requires3
%ifarch %{ix86}
Summary: 	Linux Kernel for server use with i686-up-64GB
%else
Summary: 	Linux Kernel for server use with x86_64
%endif
Group: 		System/Kernel and hardware

%ifarch{ix86}
%description -n %{kname}-server-%{buildrel}
%{kinfo1}
%{kinfo2}
%{kinfo3}
input and output, etc. This kernel is compiled for server use, single
i686 processor/core and less than 64GB RAM, using no preempt and 
cfq scheduler.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}
%else
%description -n %{kname}-server-%{buildrel}
%{kinfo1}
%{kinfo2}
%{kinfo3}
input and output, etc. This kernel is compiled for server use, single
x86_64 processor/core, using no preempt and cfq scheduler.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}
%endif



#
# kernel-tmb-server-smp: i686, smp, 64 GB /x86_64
#
%package -n %{kname}-server-smp-%{buildrel}
Version: 	%{fakever}
Release:	%{fakerel}
Provides: 	%kprovides
Requires(pre): 	%requires1
Requires(pre): 	%requires2
Requires(pre): 	%requires3
%ifarch{ix86}
Summary: 	Linux Kernel for server use with i686-smp-64GB
%else
Summary: 	Linux Kernel for server use with x86_64-smp
%endif
Group: 		System/Kernel and hardware

%ifarch{ix86}
%description -n %{kname}-server-smp-%{buildrel}
%{kinfo1}
%{kinfo2}
%{kinfo3}
input and output, etc. This kernel is compiled for server use, multiple
i686 processors/cores and less than 4GB RAM, using no preempt and 
cfq scheduler.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}
%else
%description -n %{kname}-server-smp-%{buildrel}
%{kinfo1}
%{kinfo2}
%{kinfo3}
input and output, etc. This kernel is compiled for server use, multiple
x86_64 processors/cores, using no preempt and cfq scheduler.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}
%endif



#
# kernel-tmb-source
#
%package -n %{kname}-source-%{buildrel}
Version: 	%{fakever}
Release: 	%{fakerel}
Requires: 	glibc-devel, ncurses-devel, make, gcc, perl
Summary: 	The Linux source code for %{kname}-%{buildrel}  
Group: 		Development/Kernel
Autoreqprov: 	no
Provides: 	kernel-source kernel-source-fbsplash
Conflicts: 	%{kname}-source-stripped-%{buildrel}

%description -n %{kname}-source-%{buildrel}
The kernel-source package contains the source code files for the %{ktag} 
Linux kernel. These source files are needed to build most C programs, since
they depend on the constants defined in the source code. The source
files can also be used to build a custom kernel that is better tuned to
your particular hardware, if you are so inclined (and you know what you're
doing).

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-desktop586-devel
#
%package -n	%{kname}-desktop586-devel-%{buildrel} 
Version: 	%{fakever}
Release: 	%{fakerel}
Requires: 	glibc-devel, ncurses-devel, make, gcc, perl
Summary: 	The kernel-devel files for %{kname}-desktop586-%{buildrel} 
Group: 		Development/Kernel
Autoreqprov: 	no
Provides: 	kernel-source kernel-source-fbsplash kernel-devel

%description -n %{kname}-desktop586-devel-%{buildrel}
This package contains the kernel-devel files that should be enough to build
3rdparty drivers against for use with %{kname}-desktop586-%{buildrel}.

If you want to build your own kernel, you need to install the full
%{kname}-source-%{buildrel} rpm.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-desktop586-smp-devel
#
%package -n	%{kname}-desktop586-smp-devel-%{buildrel} 
Version: 	%{fakever}
Release: 	%{fakerel}
Requires: 	glibc-devel, ncurses-devel, make, gcc, perl
Summary: 	The kernel-devel files for %{kname}-desktop586-smp-%{buildrel} 
Group: 		Development/Kernel
Autoreqprov: 	no
Provides: 	kernel-source kernel-source-fbsplash kernel-devel

%description -n %{kname}-desktop586-smp-devel-%{buildrel}
This package contains the kernel-devel files that should be enough to build
3rdparty drivers against for use with %{kname}-desktop586-smp-%{buildrel}.

If you want to build your own kernel, you need to install the full
%{kname}-source-%{buildrel} rpm.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-desktop-devel
#
%package -n	%{kname}-desktop-devel-%{buildrel} 
Version: 	%{fakever}
Release: 	%{fakerel}
Requires: 	glibc-devel, ncurses-devel, make, gcc, perl
Summary: 	The kernel-devel files for %{kname}-desktop-%{buildrel} 
Group: 		Development/Kernel
Autoreqprov: 	no
Provides: 	kernel-source kernel-source-fbsplash kernel-devel

%description -n %{kname}-desktop-devel-%{buildrel}
This package contains the kernel-devel files that should be enough to build
3rdparty drivers against for use with %{kname}-desktop-%{buildrel}.

If you want to build your own kernel, you need to install the full
%{kname}-source-%{buildrel} rpm.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-desktop-smp-devel
#
%package -n	%{kname}-desktop-smp-devel-%{buildrel} 
Version: 	%{fakever}
Release: 	%{fakerel}
Requires: 	glibc-devel, ncurses-devel, make, gcc, perl
Summary: 	The kernel-devel files for %{kname}-desktop-smp-%{buildrel} 
Group: 		Development/Kernel
Autoreqprov: 	no
Provides: 	kernel-source kernel-source-fbsplash kernel-devel

%description -n %{kname}-desktop-smp-devel-%{buildrel}
This package contains the kernel-devel files that should be enough to build
3rdparty drivers against for use with %{kname}-desktop-smp-%{buildrel}.

If you want to build your own kernel, you need to install the full
%{kname}-source-%{buildrel} rpm.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-laptop-devel
#
%package -n	%{kname}-laptop-devel-%{buildrel} 
Version: 	%{fakever}
Release: 	%{fakerel}
Requires: 	glibc-devel, ncurses-devel, make, gcc, perl
Summary: 	The kernel-devel files for %{kname}-laptop-%{buildrel} 
Group: 		Development/Kernel
Autoreqprov: 	no
Provides: 	kernel-source kernel-source-fbsplash kernel-devel

%description -n %{kname}-laptop-devel-%{buildrel}
This package contains the kernel-devel files that should be enough to build
3rdparty drivers against for use with %{kname}-laptop-%{buildrel}.

If you want to build your own kernel, you need to install the full
%{kname}-source-%{buildrel} rpm.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-laptop-smp-devel
#
%package -n	%{kname}-laptop-smp-devel-%{buildrel} 
Version: 	%{fakever}
Release: 	%{fakerel}
Requires: 	glibc-devel, ncurses-devel, make, gcc, perl
Summary: 	The kernel-devel files for %{kname}-laptop-smp-%{buildrel} 
Group: 		Development/Kernel
Autoreqprov: 	no
Provides: 	kernel-source kernel-source-fbsplash kernel-devel

%description -n %{kname}-laptop-smp-devel-%{buildrel}
This package contains the kernel-devel files that should be enough to build
3rdparty drivers against for use with %{kname}-laptop-smp-%{buildrel}.

If you want to build your own kernel, you need to install the full
%{kname}-source-%{buildrel} rpm.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-server-devel
#
%package -n	%{kname}-server-devel-%{buildrel} 
Version: 	%{fakever}
Release: 	%{fakerel}
Requires: 	glibc-devel, ncurses-devel, make, gcc, perl
Summary: 	The kernel-devel files for %{kname}-server-%{buildrel} 
Group: 		Development/Kernel
Autoreqprov: 	no
Provides: 	kernel-source kernel-source-fbsplash kernel-devel

%description -n %{kname}-server-devel-%{buildrel}
This package contains the kernel-devel files that should be enough to build
3rdparty drivers against for use with %{kname}-server-%{buildrel}.

If you want to build your own kernel, you need to install the full
%{kname}-source-%{buildrel} rpm.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-server-smp-devel
#
%package -n	%{kname}-server-smp-devel-%{buildrel} 
Version: 	%{fakever}
Release: 	%{fakerel}
Requires: 	glibc-devel, ncurses-devel, make, gcc, perl
Summary: 	The kernel-devel files for %{kname}-server-smp-%{buildrel} 
Group: 		Development/Kernel
Autoreqprov: 	no
Provides: 	kernel-source kernel-source-fbsplash kernel-devel

%description -n %{kname}-server-smp-devel-%{buildrel}
This package contains the kernel-devel files that should be enough to build
3rdparty drivers against for use with %{kname}-server-smp-%{buildrel}.

If you want to build your own kernel, you need to install the full
%{kname}-source-%{buildrel} rpm.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-doc: documentation for the Linux kernel
#
%package -n %{kname}-doc-%{buildrel}
Version: 	%{fakever}
Release: 	%{fakerel}
Summary: 	Various documentation bits found in the %{kname} source
Group: 		Books/Computer books

%description -n %{kname}-doc-%{buildrel}
This package contains documentation files from the %{kname} source. 
Various bits of information about the Linux kernel and the device drivers 
shipped with it are documented in these files. You also might want install 
this package if you need a reference to the options that can be passed to 
Linux kernel modules at load time.

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-desktop586-latest: virtual rpm
#
%package -n %{kname}-desktop586-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-desktop586
Group:   	System/Kernel and hardware
Requires: 	%{kname}-desktop586-%{buildrel}

%description -n %{kname}-desktop586-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-desktop586 installed...

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-desktop586-smp-latest: virtual rpm
#
%package -n %{kname}-desktop586-smp-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-desktop586-smp
Group:   	System/Kernel and hardware
Requires: 	%{kname}-desktop586-smp-%{buildrel}

%description -n %{kname}-desktop586-smp-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-desktop586-smp installed...

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-desktop-latest: virtual rpm
#
%package -n %{kname}-desktop-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-desktop
Group:   	System/Kernel and hardware
Requires: 	%{kname}-desktop-%{buildrel}

%description -n %{kname}-desktop-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-desktop installed...

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-desktop-smp-latest: virtual rpm
#
%package -n %{kname}-desktop-smp-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-desktop-smp
Group:   	System/Kernel and hardware
Requires: 	%{kname}-desktop-smp-%{buildrel}

%description -n %{kname}-desktop-smp-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-desktop-smp installed...

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-laptop-latest: virtual rpm
#
%package -n %{kname}-laptop-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-laptop
Group:   	System/Kernel and hardware
Requires: 	%{kname}-laptop-%{buildrel}

%description -n %{kname}-laptop-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-laptop installed...

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-laptop-smp-latest: virtual rpm
#
%package -n %{kname}-laptop-smp-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-laptop-smp
Group:   	System/Kernel and hardware
Requires: 	%{kname}-laptop-smp-%{buildrel}

%description -n %{kname}-laptop-smp-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-laptop-smp installed...

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-server-latest: virtual rpm
#
%package -n %{kname}-server-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-server
Group:   	System/Kernel and hardware
Requires: 	%{kname}-server-%{buildrel}

%description -n %{kname}-server-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-server installed...

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-server-smp-latest: virtual rpm
#
%package -n %{kname}-server-smp-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-server-smp
Group:   	System/Kernel and hardware
Requires: 	%{kname}-server-smp-%{buildrel}

%description -n %{kname}-server-smp-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-server-smp installed...

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-source-latest: virtual rpm
#
%package -n %{kname}-source-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-source
Group:   	Development/Kernel
Requires: 	%{kname}-source-%{buildrel}
Conflicts: 	%{kname}-source-stripped-latest

%description -n %{kname}-source-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-source installed...

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-desktop586-devel-latest: virtual rpm
#
%package -n %{kname}-desktop586-devel-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-desktop586-devel
Group:   	Development/Kernel
Requires: 	%{kname}-desktop586-devel-%{buildrel}
Obsoletes:	%{kname}-desktop586-headers-latest

%description -n %{kname}-desktop586-devel-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-desktop586-devel installed...

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-desktop586-smp-devel-latest: virtual rpm
#
%package -n %{kname}-desktop586-smp-devel-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-desktop586-smp-devel
Group:   	Development/Kernel
Requires: 	%{kname}-desktop586-smp-devel-%{buildrel}
Obsoletes:	%{kname}-desktop586-smp-headers-latest

%description -n %{kname}-desktop586-smp-devel-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-desktop586-smp-devel installed...

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-desktop-devel-latest: virtual rpm
#
%package -n %{kname}-desktop-devel-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-desktop-devel
Group:   	Development/Kernel
Requires: 	%{kname}-desktop-devel-%{buildrel}
Obsoletes:	%{kname}-desktop-headers-latest

%description -n %{kname}-desktop-devel-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-desktop-devel installed...

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-desktop-smp-devel-latest: virtual rpm
#
%package -n %{kname}-desktop-smp-devel-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-desktop-smp-devel
Group:   	Development/Kernel
Requires: 	%{kname}-desktop-smp-devel-%{buildrel}
Obsoletes:	%{kname}-desktop-smp-headers-latest

%description -n %{kname}-desktop-smp-devel-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-desktop-smp-devel installed...

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-laptop-devel-latest: virtual rpm
#
%package -n %{kname}-laptop-devel-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-laptop-devel
Group:   	Development/Kernel
Requires: 	%{kname}-laptop-devel-%{buildrel}
Obsoletes:	%{kname}-laptop-headers-latest

%description -n %{kname}-laptop-devel-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-laptop-devel installed...

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-laptop-smp-devel-latest: virtual rpm
#
%package -n %{kname}-laptop-smp-devel-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-laptop-smp-devel
Group:   	Development/Kernel
Requires: 	%{kname}-laptop-smp-devel-%{buildrel}
Obsoletes:	%{kname}-laptop-smp-headers-latest

%description -n %{kname}-laptop-smp-devel-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-laptop-smp-devel installed...

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-server-devel-latest: virtual rpm
#
%package -n %{kname}-server-devel-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-server-devel
Group:   	Development/Kernel
Requires: 	%{kname}-server-devel-%{buildrel}
Obsoletes:	%{kname}-server-headers-latest

%description -n %{kname}-server-devel-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-server-devel installed...

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# kernel-tmb-server-smp-devel-latest: virtual rpm
#
%package -n %{kname}-server-smp-devel-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-server-smp-devel
Group:   	Development/Kernel
Requires: 	%{kname}-server-smp-devel-%{buildrel}
Obsoletes:	%{kname}-server-smp-headers-latest

%description -n %{kname}-server-smp-devel-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-server-smp-devel installed...

%{upinfo1}
%{upinfo2}

%{info1}
%{info2}
%{info3}
%{info4}
%{info5}

%{info10}
%{info11}



#
# End packages - here begins build stage
#
%prep
%setup -q -n %top_dir_name -c

%setup -q -n %top_dir_name -D -T -a100

%define patches_dir ../%{patch_ver}/

cd %src_dir
%if %kpatch
%patch1 -p1
%endif
%if %kstable
%patch1 -p1
%endif

%{patches_dir}/scripts/apply_patches

# PATCH END



#
# Setup Begin
#

# Prepare all the variables for calling create_configs

%if %build_debug
%define debug --debug
%else
%define debug --no-debug
%endif

%{patches_dir}/scripts/create_configs %debug --user_cpu="%{target_arch}"

# make sure the kernel has the sublevel we know it has...
LC_ALL=C perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{sublevel}/" Makefile

# get rid of unwanted files
find . -name '*~' -o -name '*.orig' -o -name '*.append' |xargs rm -f



%build
# Common target directories
%define _kerneldir /usr/src/%{kversion}-%{ktag}-%{buildrpmrel}
%define _bootdir /boot
%define _modulesdir /lib/modules

# Directories definition needed for building
%define temp_root %{build_dir}/temp-root
%define temp_source %{temp_root}%{_kerneldir}
%define temp_boot %{temp_root}%{_bootdir}
%define temp_modules %{temp_root}%{_modulesdir}



PrepareKernel() {
	name=$1
	extension=$2
	echo "Make dep for kernel $extension"
	%smake -s mrproper

	# We can't use only defconfig anymore because we have the autoconf patch,
	
	if [ $name = ""]; then
	    cp arch/%{target_arch}/defconfig-maximum .config
	else
	    cp arch/%{target_arch}/defconfig-$name .config
	fi
	
# make sure EXTRAVERSION says what we want it to say
%if %kstable
	LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = .%{kstable}-$extension/" Makefile
%else
	LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -$extension/" Makefile
%endif
	%smake oldconfig
}



BuildKernel() {
	KernelVer=$1
	echo "Building kernel $KernelVer"

	%kmake all

	## Start installing stuff
	install -d %{temp_boot}
	install -m 644 System.map %{temp_boot}/System.map-$KernelVer
	install -m 644 .config %{temp_boot}/config-$KernelVer

	%ifarch sparc sparc64
		cp -f vmlinux %{temp_boot}/vmlinux-$KernelVer
	%else
		cp -f arch/%{target_arch}/boot/bzImage %{temp_boot}/vmlinuz-$KernelVer
	%endif

	# modules
	install -d %{temp_modules}/$KernelVer
	%smake INSTALL_MOD_PATH=%{temp_root} KERNELRELEASE=$KernelVer modules_install 
}



SaveDevel() {
	devel_flavour=$1
	devel_cpu=$2

	if [ "$devel_cpu" != "" ]; then
		DevelRoot=/usr/src/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}$devel_cpu
	else
		DevelRoot=/usr/src/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}
	fi
	TempDevelRoot=%{temp_root}$DevelRoot
	mkdir -p $TempDevelRoot
	for i in $(find . -name Makefile -o -name Makefile-* -o -name Makefile.*); do cp -R --parents $i $TempDevelRoot;done
	for i in $(find . -name Kconfig -o -name Kconfig.* -o -name Kbuild -o -name Kbuild.*); do cp -R --parents $i $TempDevelRoot;done
	cp -fR include $TempDevelRoot
	cp -fR scripts $TempDevelRoot
	cp -fR arch/%{target_arch}/kernel/asm-offsets.{c,s} $TempDevelRoot/arch/%{target_arch}/kernel/
	%ifarch %{ix86}
	cp -fR arch/%{target_arch}/kernel/sigframe.h $TempDevelRoot/arch/%{target_arch}/kernel/
	%endif
	cp -fR .config Module.symvers $TempDevelRoot
	cp -fR 3rdparty/mkbuild.pl $TempDevelRoot/3rdparty
	for i in alpha arm arm26 avr32 cris frv h8300 ia64 mips m32r m68k m68knommu parisc powerpc ppc s390 sh sh64 v850 xtensa; do
		rm -rf $TempDevelRoot/arch/$i
		rm -rf $TempDevelRoot/include/asm-$i
	done
	
	%ifnarch %{ix86} x86_64
		rm -rf $TempDevelRoot/arch/i386
		rm -rf $TempDevelRoot/arch/x86_64
		rm -rf $TempDevelRoot/include/asm-i386
		rm -rf $TempDevelRoot/include/asm-x86_64
	%endif
	%ifnarch sparc sparc64
		rm -rf $TempDevelRoot/arch/sparc
		rm -rf $TempDevelRoot/arch/sparc64
		rm -rf $TempDevelRoot/include/asm-sparc
		rm -rf $TempDevelRoot/include/asm-sparc64
	%endif

	# fix permissions
	chmod a+rX $TempDevelRoot

	kernel_devel_files=../kernel_devel_files.$devel_flavour$devel_cpu

### Cteate the kernel_devel_files.*
cat > $kernel_devel_files <<EOF
%defattr(-,root,root)
%dir $DevelRoot
%dir $DevelRoot/arch
%dir $DevelRoot/include
$DevelRoot/3rdparty
$DevelRoot/Documentation
%ifarch %{ix86} x86_64
$DevelRoot/arch/i386
$DevelRoot/arch/x86_64
%endif
$DevelRoot/arch/um
%ifarch sparc sparc64
$DevelRoot/arch/sparc
$DevelRoot/arch/sparc64
%endif
$DevelRoot/block
$DevelRoot/crypto
$DevelRoot/drivers
$DevelRoot/fs
$DevelRoot/include/Kbuild
$DevelRoot/include/acpi
$DevelRoot/include/asm
$DevelRoot/include/asm-generic
%ifarch %{ix86} x86_64
$DevelRoot/include/asm-i386
$DevelRoot/include/asm-x86_64
%endif
$DevelRoot/include/asm-um
%ifarch sparc sparc64
$DevelRoot/include/asm-sparc
$DevelRoot/include/asm-sparc64
%endif
$DevelRoot/include/config
$DevelRoot/include/crypto
$DevelRoot/include/keys
$DevelRoot/include/linux
$DevelRoot/include/math-emu
$DevelRoot/include/media
$DevelRoot/include/mtd
$DevelRoot/include/net
$DevelRoot/include/pcmcia
$DevelRoot/include/rdma
$DevelRoot/include/rxrpc
$DevelRoot/include/scsi
$DevelRoot/include/sound
$DevelRoot/include/video
$DevelRoot/init
$DevelRoot/ipc
$DevelRoot/kernel
$DevelRoot/lib
$DevelRoot/mm
$DevelRoot/net
$DevelRoot/scripts
$DevelRoot/security
$DevelRoot/sound
$DevelRoot/usr
$DevelRoot/.config
$DevelRoot/Kbuild
$DevelRoot/Makefile
$DevelRoot/Module.symvers
%doc README.Mandriva_Linux_%{ktag}
%doc README.kernel-%{ktag}-sources
%doc README.urpmi
EOF


### Create -devel Post script on the fly
cat > $kernel_devel_files-post <<EOF
if [ -d /lib/modules/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}$devel_cpu ]; then
	ln -sf $DevelRoot /lib/modules/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}$devel_cpu/build
	ln -sf $DevelRoot /lib/modules/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}$devel_cpu/source
fi
EOF


### Create -devel Preun script on the fly
cat > $kernel_devel_files-preun <<EOF
if [ -L /lib/modules/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}$devel_cpu/build ]; then
	rm -f /lib/modules/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}$devel_cpu/build
fi
if [ -L /lib/modules/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}$devel_cpu/source ]; then
	rm -f /lib/modules/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}$devel_cpu/source
fi
exit 0
EOF
}



CreateFiles() {
	kernel_flavour=$1
	kernel_cpu=$2
	
	kernel_files=../kernel_files.$kernel_flavour$kernel_cpu
	
### Create the kernel_files.*
cat > $kernel_files <<EOF
%defattr(-,root,root)
%{_bootdir}/System.map-%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu
%{_bootdir}/config-%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu
%ifarch sparc sparc64
%{_bootdir}/vmlinux-%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu
%else
%{_bootdir}/vmlinuz-%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu
%endif
%dir %{_modulesdir}/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu/
%{_modulesdir}/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu/kernel
%{_modulesdir}/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu/modules.*
%doc README.Mandriva_Linux_%{ktag}
%doc README.kernel-%{ktag}-sources
%doc README.urpmi
EOF


### Create kernel Post script
cat > $kernel_files-post <<EOF
/sbin/installkernel -L %{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu
if [ -x /sys/devices/platform/i8042 ]; then
	grep -q -s "psmouse" /etc/modprobe.preload || \
	/bin/echo -e "\npsmouse" >> /etc/modprobe.preload
fi
%ifarch %{ix86} x86_64
grep -q -s "pcspkr" /etc/modprobe.preload || \
/bin/echo -e "\npcspkr" >> /etc/modprobe.preload
%endif
pushd /boot > /dev/null
%ifarch sparc sparc64
if [ -L vmlinux-%{ktag}-$kernel_flavour$kernel_cpu ]; then
	rm -f vmlinux-%{ktag}-$kernel_flavour$kernel_cpu
fi
ln -sf vmlinux-%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu vmlinux-%{ktag}-$kernel_flavour$kernel_cpu
%else
if [ -L vmlinuz-%{ktag}-$kernel_flavour$kernel_cpu ]; then
	rm -f vmlinuz-%{ktag}-$kernel_flavour$kernel_cpu
fi
ln -sf vmlinuz-%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu vmlinuz-%{ktag}-$kernel_flavour$kernel_cpu
%endif
if [ -L initrd-%{ktag}-$kernel_flavour$kernel_cpu.img ]; then
	rm -f initrd-%{ktag}-$kernel_flavour$kernel_cpu.img
fi
ln -sf initrd-%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu.img initrd-%{ktag}-$kernel_flavour$kernel_cpu.img
popd > /dev/null
%if %build_devel
if [ -d /usr/src/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu ]; then
	ln -sf /usr/src/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu /lib/modules/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}$devel_cpu/build
	ln -sf /usr/src/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu /lib/modules/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}$devel_cpu/source
fi
%endif
EOF


### Create kernel Preun script on the fly
cat > $kernel_files-preun <<EOF
/sbin/installkernel -R %{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu
pushd /boot > /dev/null
%ifarch sparc sparc64
if [ -L vmlinux-%{ktag}-$kernel_flavour$kernel_cpu ]; then
	if [ "ls -l vmlinux-%{ktag}-$kernel_flavour$kernel_cpu 2>/dev/null| awk '{ print $11 }'" = "vmlinux-%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu" ]; then
		rm -f vmlinux-%{ktag}-$kernel_flavour$kernel_cpu
	fi
fi
%else
if [ -L vmlinuz-%{ktag}-$kernel_flavour$kernel_cpu ]; then
	if [ "ls -l vmlinuz-%{ktag}-$kernel_flavour$kernel_cpu 2>/dev/null| awk '{ print $11 }'" = "vmlinuz-%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu" ]; then
		rm -f vmlinuz-%{ktag}-$kernel_flavour$kernel_cpu
	fi
fi
%endif
if [ -L initrd-%{ktag}-$kernel_flavour$kernel_cpu.img ]; then
	if [ "ls -l initrd-%{ktag}-$kernel_flavour$kernel_cpu.img 2>/dev/null| awk '{ print $11 }'" = "initrd-%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu.img" ]; then
		rm -f initrd-%{ktag}-$kernel_flavour$kernel_cpu.img
	fi
fi
popd > /dev/null
%if %build_devel
if [ -L /lib/modules/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu/build ]; then
	rm -f /lib/modules/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu/build
fi
if [ -L /lib/modules/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu/source ]; then
	rm -f /lib/modules/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu/source
fi
%endif
exit 0
EOF


### Create kernel Postun script on the fly
cat > $kernel_files-postun <<EOF
/sbin/kernel_remove_initrd %{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}$kernel_cpu
EOF
}



CreateKernel() {
	flavour=$1
	processor=$2

	PrepareKernel $flavour$processor %{ktag}-$flavour-%{buildrpmrel}$processor

	BuildKernel %{kversion}-%{ktag}-$flavour-%{buildrpmrel}$processor
	%if %build_devel
		SaveDevel $flavour $processor
	%endif
	CreateFiles $flavour $processor
}



###
# DO it...
###



# Create a simulacro of buildroot
rm -rf %{temp_root}
install -d %{temp_root}



#make sure we are in the directory
cd %src_dir

%ifarch %{ix86}
%if %build_desktop586_smp
CreateKernel desktop smp-i586
%endif

%if %build_desktop586_up
CreateKernel desktop -i586
%endif
%endif

%if %build_desktop_smp
CreateKernel desktop smp
%endif

%if %build_desktop_up
CreateKernel desktop ""
%endif

%if %build_laptop_smp
CreateKernel laptop smp
%endif

%if %build_laptop_up
CreateKernel laptop ""
%endif

%if %build_server_smp
CreateKernel server smp
%endif

%if %build_server_up
CreateKernel server ""
%endif



# We don't make to repeat the depend code at the install phase
%if %build_source
    PrepareKernel "" %{buildrpmrel}%{ktag}custom
%smake -s prepare
%smake -s scripts
%endif



###
### install
###
%install
install -m 644 %{SOURCE4}  .
install -m 644 %{SOURCE5}  .
install -m 644 %{SOURCE6}  README.urpmi

cd %src_dir



# Directories definition needed for installing
%define target_source %{buildroot}%{_kerneldir}
%define target_boot %{buildroot}%{_bootdir}
%define target_modules %{buildroot}%{_modulesdir}



# We want to be able to test several times the install part
rm -rf %{buildroot}
cp -a %{temp_root} %{buildroot}



# Create directories infastructure
%if %build_source
install -d %{target_source} 

tar cf - . | tar xf - -C %{target_source}
chmod -R a+rX %{target_source}



# we remove all the source files that we don't ship
# first architecture files
for i in alpha arm arm26 avr32 cris frv h8300 ia64 mips m32r m68k m68knommu parisc powerpc ppc s390 sh sh64 v850 xtensa; do
	rm -rf %{target_source}/arch/$i
	rm -rf %{target_source}/include/asm-$i
done

%ifnarch %{ix86} x86_64
	rm -rf %{target_source}/arch/i386
	rm -rf %{target_source}/arch/x86_64
	rm -rf %{target_source}/include/asm-i386
	rm -rf %{target_source}/include/asm-x86_64
%endif
%ifnarch sparc sparc64
	rm -rf %{target_source}/arch/sparc
	rm -rf %{target_source}/arch/sparc64
	rm -rf %{target_source}/include/asm-sparc
	rm -rf %{target_source}/include/asm-sparc64
%endif

# other misc files
rm -f %{target_source}/{.config.old,.config.cmd}

#endif %build_source
%endif



# gzipping modules
find %{target_modules} -name "*.ko" | xargs gzip -9



# We used to have a copy of PrepareKernel here
# Now, we make sure that the thing in the linux dir is what we want it to be
for i in %{target_modules}/*; do
  rm -f $i/build $i/source $i/modules.*
done



# sniff, if we gzipped all the modules, we change the stamp :(
# we really need the depmod -ae here
pushd %{target_modules}
for i in *; do
	/sbin/depmod-25 -u -ae -b %{buildroot} -r -F %{target_boot}/System.map-$i $i
	echo $?
done

for i in *; do
	pushd $i
	echo "Creating module.description for $i"
	modules=`find . -name "*.ko.gz"`
	echo $modules | xargs /sbin/modinfo-25 \
	| perl -lne 'print "$name\t$1" if $name && /^description:\s*(.*)/; $name = $1 if m!^filename:\s*(.*)\.k?o!; $name =~ s!.*/!!' > modules.description
	popd
done
popd



###
### clean
###
%clean
rm -rf %{buildroot}



# We don't want to remove this, the whole reason of its existence is to be 
# able to do several rpm --short-circuit -bi for testing install 
# phase without repeating compilation phase
#rm -rf %{temp_root} 



###
### scripts
###

# desktop586 scripts
%post -n %{kname}-desktop586-%{buildrel} -f kernel_files.desktop-i586-post

%preun -n %{kname}-desktop586-%{buildrel} -f kernel_files.desktop-i586-preun

%postun -n %{kname}-desktop586-%{buildrel} -f kernel_files.desktop-i586-postun



# desktop586-smp scripts
%post -n %{kname}-desktop586-smp-%{buildrel} -f kernel_files.desktopsmp-i586-post

%preun -n %{kname}-desktop586-smp-%{buildrel} -f kernel_files.desktopsmp-i586-preun

%postun -n %{kname}-desktop586-smp-%{buildrel} -f kernel_files.desktopsmp-i586-postun



# desktop scripts
%post -n %{kname}-desktop-%{buildrel} -f kernel_files.desktop-post

%preun -n %{kname}-desktop-%{buildrel} -f kernel_files.desktop-preun

%postun -n %{kname}-desktop-%{buildrel} -f kernel_files.desktop-postun



# desktop-smp scripts
%post -n %{kname}-desktop-smp-%{buildrel} -f kernel_files.desktopsmp-post

%preun -n %{kname}-desktop-smp-%{buildrel} -f kernel_files.desktopsmp-preun

%postun -n %{kname}-desktop-smp-%{buildrel} -f kernel_files.desktopsmp-postun



# laptop scripts
%post -n %{kname}-laptop-%{buildrel} -f kernel_files.laptop-post

%preun -n %{kname}-laptop-%{buildrel} -f kernel_files.laptop-preun

%postun -n %{kname}-laptop-%{buildrel} -f kernel_files.laptop-postun



# laptop-smp scripts
%post -n %{kname}-laptop-smp-%{buildrel} -f kernel_files.laptopsmp-post

%preun -n %{kname}-laptop-smp-%{buildrel} -f kernel_files.laptopsmp-preun

%postun -n %{kname}-laptop-smp-%{buildrel} -f kernel_files.laptopsmp-postun



# server scripts
%post -n %{kname}-server-%{buildrel} -f kernel_files.server-post

%preun -n %{kname}-server-%{buildrel} -f kernel_files.server-preun

%postun -n %{kname}-server-%{buildrel} -f kernel_files.server-postun



# server-smp scripts
%post -n %{kname}-server-smp-%{buildrel} -f kernel_files.serversmp-post

%preun -n %{kname}-server-smp-%{buildrel} -f kernel_files.serversmp-preun

%postun -n %{kname}-server-smp-%{buildrel} -f kernel_files.serversmp-postun



### kernel-desktop586-devel
%post -n %{kname}-desktop586-devel-%{buildrel} -f kernel_devel_files.desktop-i586-post

%preun -n %{kname}-desktop586-devel-%{buildrel} -f kernel_devel_files.desktop-i586-preun



### kernel-desktop586-smp-devel
%post -n %{kname}-desktop586-smp-devel-%{buildrel} -f kernel_devel_files.desktopsmp-i586-post

%preun -n %{kname}-desktop586-smp-devel-%{buildrel} -f kernel_devel_files.desktopsmp-i586-preun



### kernel-desktop-devel
%post -n %{kname}-desktop-devel-%{buildrel} -f kernel_devel_files.desktop-post

%preun -n %{kname}-desktop-devel-%{buildrel} -f kernel_devel_files.desktop-preun



### kernel-desktop-smp-devel
%post -n %{kname}-desktop-smp-devel-%{buildrel} -f kernel_devel_files.desktopsmp-post

%preun -n %{kname}-desktop-smp-devel-%{buildrel} -f kernel_devel_files.desktopsmp-preun



### kernel-laptop-devel
%post -n %{kname}-laptop-devel-%{buildrel} -f kernel_devel_files.laptop-post

%preun -n %{kname}-laptop-devel-%{buildrel} -f kernel_devel_files.laptop-preun



### kernel-laptop-smp-devel
%post -n %{kname}-laptop-smp-devel-%{buildrel} -f kernel_devel_files.laptopsmp-post

%preun -n %{kname}-laptop-smp-devel-%{buildrel} -f kernel_devel_files.laptopsmp-preun



### kernel-server-devel
%post -n %{kname}-server-devel-%{buildrel} -f kernel_devel_files.server-post

%preun -n %{kname}-server-devel-%{buildrel} -f kernel_devel_files.server-preun



### kernel-server-smp-devel
%post -n %{kname}-server-smp-devel-%{buildrel} -f kernel_devel_files.serversmp-post

%preun -n %{kname}-server-smp-devel-%{buildrel} -f kernel_devel_files.serversmp-preun



###
### file lists
###

%ifarch %{ix86}
%if %build_desktop586_up
%files -n %{kname}-desktop586-%{buildrel} -f kernel_files.desktop-i586
%endif

%if %build_desktop586_smp
%files -n %{kname}-desktop586-smp-%{buildrel} -f kernel_files.desktopsmp-i586
%endif
%endif

%if %build_desktop_up
%files -n %{kname}-desktop-%{buildrel} -f kernel_files.desktop
%endif

%if %build_desktop_smp
%files -n %{kname}-desktop-smp-%{buildrel} -f kernel_files.desktopsmp
%endif

%if %build_laptop_up
%files -n %{kname}-laptop-%{buildrel} -f kernel_files.laptop
%endif

%if %build_laptop_smp
%files -n %{kname}-laptop-smp-%{buildrel} -f kernel_files.laptopsmp
%endif

%if %build_server_up
%files -n %{kname}-server-%{buildrel} -f kernel_files.server
%endif

%if %build_server_smp
%files -n %{kname}-server-smp-%{buildrel} -f kernel_files.serversmp
%endif

%if %build_source
%files -n %{kname}-source-%{buildrel}
%defattr(-,root,root)
%dir %{_kerneldir}
%dir %{_kerneldir}/arch
%dir %{_kerneldir}/include
%{_kerneldir}/3rdparty
%{_kerneldir}/Documentation
%ifarch %{ix86} x86_64
%{_kerneldir}/arch/i386
%{_kerneldir}/arch/x86_64
%endif
%ifarch sparc sparc64
%{_kerneldir}/arch/sparc
%{_kerneldir}/arch/sparc64
%endif
%{_kerneldir}/arch/um
%{_kerneldir}/block
%{_kerneldir}/crypto
%{_kerneldir}/drivers
%{_kerneldir}/fs
%{_kerneldir}/include/Kbuild
%{_kerneldir}/include/acpi
%{_kerneldir}/include/asm
%{_kerneldir}/include/asm-generic
%ifarch %{ix86} x86_64
%{_kerneldir}/include/asm-i386
%{_kerneldir}/include/asm-x86_64
%endif
%ifarch sparc sparc64
%{_kerneldir}/include/asm-sparc
%{_kerneldir}/include/asm-sparc64
%endif
%{_kerneldir}/include/asm-um
%{_kerneldir}/include/config
%{_kerneldir}/include/crypto
%{_kerneldir}/include/keys
%{_kerneldir}/include/linux
%{_kerneldir}/include/math-emu
%{_kerneldir}/include/media
%{_kerneldir}/include/mtd
%{_kerneldir}/include/net
%{_kerneldir}/include/pcmcia
%{_kerneldir}/include/rdma
%{_kerneldir}/include/rxrpc
%{_kerneldir}/include/scsi
%{_kerneldir}/include/sound
%{_kerneldir}/include/video
%{_kerneldir}/init
%{_kerneldir}/ipc
%{_kerneldir}/kernel
%{_kerneldir}/lib
%{_kerneldir}/mm
%{_kerneldir}/net
%{_kerneldir}/scripts
%{_kerneldir}/security
%{_kerneldir}/sound
%{_kerneldir}/usr
%{_kerneldir}/.config
%{_kerneldir}/.gitignore
%{_kerneldir}/COPYING
%{_kerneldir}/CREDITS
%{_kerneldir}/Kbuild
%{_kerneldir}/MAINTAINERS
%{_kerneldir}/Makefile
%{_kerneldir}/README
%{_kerneldir}/REPORTING-BUGS
%doc README.Mandriva_Linux_%{ktag}
%doc README.kernel-%{ktag}-sources
%doc README.urpmi
#endif build_source
%endif

%if %build_devel
%ifarch %{ix86}
%if %build_desktop586_up
%files -n %{kname}-desktop586-devel-%{buildrel} -f kernel_devel_files.desktop-i586
%endif

%if %build_desktop586_smp
%files -n %{kname}-desktop586-smp-devel-%{buildrel} -f kernel_devel_files.desktopsmp-i586
%endif
%endif

%if %build_desktop_up
%files -n %{kname}-desktop-devel-%{buildrel} -f kernel_devel_files.desktop
%endif

%if %build_desktop_smp
%files -n %{kname}-desktop-smp-devel-%{buildrel} -f kernel_devel_files.desktopsmp
%endif

%if %build_laptop_up
%files -n %{kname}-laptop-devel-%{buildrel} -f kernel_devel_files.laptop
%endif

%if %build_laptop_smp
%files -n %{kname}-laptop-smp-devel-%{buildrel} -f kernel_devel_files.laptopsmp
%endif

%if %build_server_up
%files -n %{kname}-server-devel-%{buildrel} -f kernel_devel_files.server
%endif

%if %build_server_smp
%files -n %{kname}-server-smp-devel-%{buildrel} -f kernel_devel_files.serversmp
%endif
#endif build_devel
%endif

%if %build_doc
%files -n %{kname}-doc-%{buildrel}
%defattr(-,root,root)
%doc linux-%{tar_ver}/Documentation/*
%endif

%ifarch %{ix86}
%if %build_desktop586_up
%files -n %{kname}-desktop586-latest
%defattr(-,root,root)
%endif

%if %build_desktop586_smp
%files -n %{kname}-desktop586-smp-latest
%defattr(-,root,root)
%endif
%endif

%if %build_desktop_up
%files -n %{kname}-desktop-latest
%defattr(-,root,root)
%endif

%if %build_desktop_smp
%files -n %{kname}-desktop-smp-latest
%defattr(-,root,root)
%endif

%if %build_laptop_up
%files -n %{kname}-laptop-latest
%defattr(-,root,root)
%endif

%if %build_laptop_smp
%files -n %{kname}-laptop-smp-latest
%defattr(-,root,root)
%endif

%if %build_server_up
%files -n %{kname}-server-latest
%defattr(-,root,root)
%endif

%if %build_server_smp
%files -n %{kname}-server-smp-latest
%defattr(-,root,root)
%endif

%if %build_source
%files -n %{kname}-source-latest
%defattr(-,root,root)
%endif

%if %build_devel
%ifarch %{ix86}
%if %build_desktop586_up
%files -n %{kname}-desktop586-devel-latest
%defattr(-,root,root)
%endif

%if %build_desktop586_smp
%files -n %{kname}-desktop586-smp-devel-latest
%defattr(-,root,root)
%endif
%endif

%if %build_desktop_up
%files -n %{kname}-desktop-devel-latest
%defattr(-,root,root)
%endif

%if %build_desktop_smp
%files -n %{kname}-desktop-smp-devel-latest
%defattr(-,root,root)
%endif

%if %build_laptop_up
%files -n %{kname}-laptop-devel-latest
%defattr(-,root,root)
%endif

%if %build_laptop_smp
%files -n %{kname}-laptop-smp-devel-latest
%defattr(-,root,root)
%endif

%if %build_server_up
%files -n %{kname}-server-devel-latest
%defattr(-,root,root)
%endif

%if %build_server_smp
%files -n %{kname}-server-smp-devel-latest
%defattr(-,root,root)
%endif
#endif build_devel
%endif



