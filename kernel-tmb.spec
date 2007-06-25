#
# *tmb* series kernels now use kernel.org versioning
#
%define kernelversion	2
%define patchlevel	6
%define sublevel	22

# kernel Makefile extraversion is substituted by 
# kpatch/kstable wich are either 0 (empty), pre/rc (kpatch) or stable release (kstable)
%define kpatch		rc6
%define kstable		0

# this is the releaseversion
%define kbuild		1

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
%define patch_ver 	%{kversion}-%{kpatch}-%{ktag}%{kbuild}
%else
%if %kstable
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}.%{kstable}
%define tar_ver   	%{kernelversion}.%{patchlevel}.%{sublevel}
%else
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}
%define tar_ver   	%{kversion}
%endif
%define patch_ver 	%{kversion}-%{ktag}%{kbuild}
%endif
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
%define build_desktop586	1
%endif

# Build mm (i686 / 4GB) / x86_64 / sparc64 sets
%define build_desktop		1

# Build laptop (i686 / 4GB)/ x86_64
%ifarch %{ix86} x86_64
%define build_laptop		1
%endif

# Build server (i686 / 64GB)/x86_64 / sparc64 sets
%define build_server		1

# End of user definitions
%{?_without_desktop586: %global build_desktop586 0}
%{?_without_desktop: %global build_desktop 0}
%{?_without_laptop: %global build_laptop 0}
%{?_without_server: %global build_server 0}
%{?_without_doc: %global build_doc 0}
%{?_without_source: %global build_source 0}
%{?_without_devel: %global build_devel 0}
%{?_without_debug: %global build_debug 0}

%{?_with_desktop586: %global build_desktop586 1}
%{?_with_desktop: %global build_desktop 1}
%{?_with_laptop: %global build_laptop 1}
%{?_with_server: %global build_server 1}
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
Patch1:		ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}.bz2
Source10: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}.bz2.sign
%endif
%if %kstable
Patch1:   	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/patch-%{kversion}.bz2
Source10: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/patch-%{kversion}.bz2.sign
%endif

#END
####################################################################

# Defines for the things that are needed for all the kernels
#
%define common_description_kernel The kernel package contains the Linux kernel (vmlinuz), the core of your \
Mandriva Linux operating system.  The kernel handles the basic functions \
of the operating system:  memory allocation, process allocation, device \
input and output, etc.

%define common_description_info For instructions for update, see:	\
http://www.mandriva.com/security/kernelupdate				\
									\
The %{ktag} kernels is an experimental kernel based on the kernel.org	\
kernels with added patches. Some of them may/will never end up in	\
the main kernels due to their experimental nature. Some refer to	\
this kernel as a 'hackkernel' ...					\
Use these kernels at your own risk !!					\
									\
If you want more info on the various %{kname} flavours, please visit:	\
http://www.iki.fi/tmb/Kernels/

### Global Requires/Provides
%define requires1 	mkinitrd >= 4.2.17-%mkrel 20
%define requires2 	bootloader-utils >= 1.12-%mkrel 1
%define requires3 	sysfsutils >= 1.3.0-%mkrel 1 module-init-tools >= 3.2-0.pre8.%mkrel 2

%define kprovides 	%{kname} = %{kverrel}, kernel = %{tar_ver}

BuildRoot: 		%{_tmppath}/%{kname}-%{kversion}-%{_arch}-build
Autoreqprov: 		no
BuildRequires: 		gcc >= 4.0.1-%mkrel 5 module-init-tools >= 3.2-0.pre8.%mkrel 2

%description
%common_description_kernel

%common_description_info


# mkflavour() name flavour processor
# name: the flavour name in the package name
# flavour: first parameter of CreateKernel()
%define mkflavour()					\
%package -n %{kname}-%{1}-%{buildrel}			\
Version:	%{fakever}				\
Release:	%{fakerel}				\
Provides:	%kprovides				\
Requires(pre):	%requires1 %requires2 %requires3	\
Summary:	%{expand:%{summary_%(echo %{1})}}	\
Group:		System/Kernel and hardware		\
%description -n %{kname}-%{1}-%{buildrel}		\
%common_description_kernel %{expand:%{info_%(echo %{1})}} \
							\
%common_description_info				\
							\
%package -n	%{kname}-%{1}-devel-%{buildrel}		\
Version:	%{fakever}				\
Release:	%{fakerel}				\
Requires:	glibc-devel ncurses-devel make gcc perl	\
Summary:	The kernel-devel files for %{kname}-%{1}-%{buildrel} \
Group:		Development/Kernel			\
Provides:	kernel-devel = %{kverrel} 		\
%description -n %{kname}-%{1}-devel-%{buildrel}		\
This package contains the kernel-devel files that should be enough to build \
3rdparty drivers against for use with %{kname}-%{1}-%{buildrel}. \
							\
If you want to build your own kernel, you need to install the full \
%{kname}-source-%{buildrel} rpm.			\
							\
%common_description_info				\
							\
%package -n %{kname}-%{1}-latest			\
Version:	%{kversion}				\
Release:	%{rpmrel}				\
Summary:	Virtual rpm for latest %{kname}-%{1}	\
Group:		System/Kernel and hardware		\
Requires:	%{kname}-%{1}-%{buildrel}		\
Obsoletes:	%{kname}-%{1}-smp-latest <= 2.6.22-0.rc5.%{expand:%mkrel 1} \
%description -n %{kname}-%{1}-latest			\
This package is a virtual rpm that aims to make sure you always have the \
latest %{kname}-%{1} installed...			\
							\
%common_description_info				\
							\
%package -n %{kname}-%{1}-devel-latest			\
Version:	%{kversion}				\
Release:	%{rpmrel}				\
Summary:	Virtual rpm for latest %{kname}-%{1}-devel \
Group:		Development/Kernel			\
Requires:	%{kname}-%{1}-devel-%{buildrel}		\
Obsoletes:	%{kname}-%{1}-smp-devel-latest <= 2.6.22-0.rc5.%{expand:%mkrel 1} \
%description -n %{kname}-%{1}-devel-latest		\
This package is a virtual rpm that aims to make sure you always have the \
latest %{kname}-%{1}-devel installed...			\
							\
%common_description_info				\
							\
%post -n %{kname}-%{1}-%{buildrel} -f kernel_files.%{1}-post \
%preun -n %{kname}-%{1}-%{buildrel} -f kernel_files.%{1}-preun \
%postun -n %{kname}-%{1}-%{buildrel} -f kernel_files.%{1}-postun \
							\
%post -n %{kname}-%{1}-devel-%{buildrel} -f kernel_devel_files.%{1}-post \
%preun -n %{kname}-%{1}-devel-%{buildrel} -f kernel_devel_files.%{1}-preun \
							\
%files -n %{kname}-%{1}-%{buildrel} -f kernel_files.%{1} \
%files -n %{kname}-%{1}-latest				\
%defattr(-,root,root)					\
							\
%if %build_devel					\
%files -n %{kname}-%{1}-devel-%{buildrel} -f kernel_devel_files.%{1} \
%files -n %{kname}-%{1}-devel-latest			\
%defattr(-,root,root)					\
%endif


%ifarch %{ix86}
#
# kernel-desktop586: i586, smp-alternatives, 1GB
#

%if %build_desktop586
%define summary_desktop586 Linux kernel for desktop use with i586 & 1GB RAM
%define info_desktop586 This kernel is compiled for desktop use, single or \
multiple i586 processor(s)/core(s) and less than 1GB RAM (usually 870-900MB \
detected), using voluntary preempt, CFS cpu scheduler and cfq i/o scheduler. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%mkflavour desktop586
%endif
%endif

#
# kernel-desktop: i686, smp-alternatives, 4 GB / x86_64
#

%if %build_desktop
%ifarch %{ix86}
%define summary_desktop Linux Kernel for desktop use with i686 & 4GB RAM
%define info_desktop This kernel is compiled for desktop use, single or \
multiple i686 processor(s)/core(s) and less than 4GB RAM, using voluntary \
preempt, CFS cpu scheduler and cfq i/o scheduler. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%else
%define summary_desktop Linux Kernel for desktop use with %{_arch}
%define info_desktop This kernel is compiled for desktop use, single or \
multiple %{_arch} processor(s)/core(s), using voluntary preempt, CFS cpu \
scheduler and cfq i/o scheduler. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%endif
%mkflavour desktop
%endif

#
# kernel-laptop: i686, smp-alternatives, 4GB / x86_64
#

%if %build_laptop
%ifarch %{ix86}
%define summary_laptop Linux kernel for laptop use with i686-up/smp-4GB
%define info_laptop This kernel is compiled for laptop use, single or \
multiple i686 processor(s)/core(s) and less than 4GB RAM, using HZ_100 \
to save battery, voluntary preempt, CFS cpu scheduler, cfq i/o scheduler \
and some other laptop-specific optimizations. If you want to sacrifice \
battery life for performance, you better use the %{kname}-desktop. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%else
%define summary_laptop Linux kernel for laptop use with %{_arch}
%define info_laptop This kernel is compiled for laptop use, single or \
multiple %{_arch} processor(s)/core(s), using HZ_100 to save battery, \
voluntary preempt, CFS cpu scheduler, cfq i/o scheduler and some other \
laptop-specific optimizations. If you want to sacrifice battery life for \
performance, you better use the %{kname}-desktop. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%endif
%mkflavour laptop
%endif

#
# kernel-server: i686, smp-alternatives, 64 GB /x86_64
#

%if %build_server
%ifarch %{ix86}
%define summary_server Linux Kernel for server use with i686  & 64GB RAM
%define info_server This kernel is compiled for server use, single or \
multiple i686 processor(s)/core(s) and up to 64GB RAM using PAE, using \
no preempt, CFS cpu scheduler and cfq i/o scheduler. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%else
%define summary_server Linux Kernel for server use with %{_arch}
%define info_server This kernel is compiled for server use, single or \
multiple %{_arch} processor(s)/core(s), using no preempt, CFS cpu scheduler \
and cfq i/o scheduler. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%endif
%mkflavour server
%endif

#
# kernel-source
#
%package -n %{kname}-source-%{buildrel}
Version: 	%{fakever}
Release: 	%{fakerel}
Requires: 	glibc-devel, ncurses-devel, make, gcc, perl
Summary: 	The Linux source code for %{kname}-%{buildrel}  
Group: 		Development/Kernel
Autoreqprov: 	no
Provides: 	kernel-source = %{kverrel}, kernel-source-fbsplash, kernel-devel = %{kverrel}

%description -n %{kname}-source-%{buildrel}
The %{kname}-source package contains the source code files for the %{ktag}
series Linux kernel. Theese source files are only needed if you want to 
build your own custom kernel that is better tuned to your particular hardware.

If you only want the files needed to build 3rdparty (nVidia, Ati, dkms-*,...)
drivers against, install the *-devel-* rpm that is matching your kernel.

%common_description_info

%post -n %{kname}-source-%{buildrel}
for i in /lib/modules/%{kversion}-%{ktag}-*-%{buildrpmrel}; do
        if [ -d $i ]; then
		rm -f $i/{build,source}
                ln -sf /usr/src/%{kversion}-%{ktag}-%{buildrpmrel} $i/build
                ln -sf /usr/src/%{kversion}-%{ktag}-%{buildrpmrel} $i/source
        fi
done

%preun -n %{kname}-source-%{buildrel}
for i in /lib/modules/%{kversion}-%{ktag}-*-%{buildrpmrel}/{build,source}; do
	if [ -L $i ]; then
		rm -f $i
	fi
done
exit 0

#
# kernel-source-latest: virtual rpm
#
%package -n %{kname}-source-latest
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-source
Group:   	Development/Kernel
Requires: 	%{kname}-source-%{buildrel}

%description -n %{kname}-source-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-source installed...

%common_description_info

#
# kernel-doc: documentation for the Linux kernel
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

%common_description_info

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

# Start installing stuff
	install -d %{temp_boot}
	install -m 644 System.map %{temp_boot}/System.map-$KernelVer
	install -m 644 .config %{temp_boot}/config-$KernelVer

	%ifarch sparc sparc64
		gzip -9c vmlinux > %{temp_boot}/vmlinuz-$KernelVer
	%else
		cp -f arch/%{target_arch}/boot/bzImage %{temp_boot}/vmlinuz-$KernelVer
	%endif

	# modules
	install -d %{temp_modules}/$KernelVer
	%smake INSTALL_MOD_PATH=%{temp_root} KERNELRELEASE=$KernelVer modules_install 
}


SaveDevel() {
	devel_flavour=$1

	DevelRoot=/usr/src/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}
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
	
# Needed for truecrypt build (Danny)
	cp -fR drivers/md/dm.h $TempDevelRoot/drivers/md/
	
	for i in alpha arm arm26 avr32 blackfin cris frv h8300 ia64 mips m32r m68k m68knommu parisc powerpc ppc s390 sh sh64 v850 xtensa; do
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

### FIXME MDV bugs #29744, #29074, will be removed when fixed upstream
        mkdir -p $TempDevelRoot/arch/s390/crypto/
        cp -fR arch/s390/crypto/Kconfig $TempDevelRoot/arch/s390/crypto/

# fix permissions
	chmod -R a+rX $TempDevelRoot

	kernel_devel_files=../kernel_devel_files.$devel_flavour
	

### Cteate the kernel_devel_files.*
# defattr sets the tree to readonly to try and work around broken dkms & co
cat > $kernel_devel_files <<EOF
#defattr(0444,root,root,0555)
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
### FIXME MDV bugs #29744, #29074, will be removed when fixed upstream
$DevelRoot/arch/s390
%ifarch sparc sparc64
$DevelRoot/arch/sparc
$DevelRoot/arch/sparc64
%endif
$DevelRoot/arch/um
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
%ifarch sparc sparc64
$DevelRoot/include/asm-sparc
$DevelRoot/include/asm-sparc64
%endif
$DevelRoot/include/asm-um
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
if [ -d /lib/modules/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel} ]; then
	ln -sf $DevelRoot /lib/modules/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}/build
	ln -sf $DevelRoot /lib/modules/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}/source
fi
EOF


### Create -devel Preun script on the fly
cat > $kernel_devel_files-preun <<EOF
if [ -L /lib/modules/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}/build ]; then
	rm -f /lib/modules/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}/build
fi
if [ -L /lib/modules/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}$devel_cpu/source ]; then
	rm -f /lib/modules/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}/source
fi
exit 0
EOF
}


CreateFiles() {
	kernel_flavour=$1
	
	kernel_files=../kernel_files.$kernel_flavour
	
### Create the kernel_files.*
cat > $kernel_files <<EOF
%defattr(-,root,root)
%{_bootdir}/System.map-%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}
%{_bootdir}/config-%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}
%{_bootdir}/vmlinuz-%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}
%dir %{_modulesdir}/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}/
%{_modulesdir}/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}/kernel
%{_modulesdir}/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}/modules.*
%doc README.Mandriva_Linux_%{ktag}
%doc README.kernel-%{ktag}-sources
%doc README.urpmi
EOF


### Create kernel Post script
cat > $kernel_files-post <<EOF
/sbin/installkernel -L %{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}
if [ -x /sys/devices/platform/i8042 ]; then
	grep -q -s "psmouse" /etc/modprobe.preload || \
	/bin/echo -e "\npsmouse" >> /etc/modprobe.preload
fi
%ifarch %{ix86} x86_64
grep -q -s "pcspkr" /etc/modprobe.preload || \
/bin/echo -e "\npcspkr" >> /etc/modprobe.preload
%endif
pushd /boot > /dev/null
if [ -L vmlinuz-%{ktag}-$kernel_flavour ]; then
	rm -f vmlinuz-%{ktag}-$kernel_flavour
fi
ln -sf vmlinuz-%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel} vmlinuz-%{ktag}-$kernel_flavour
if [ -L initrd-%{ktag}-$kernel_flavour.img ]; then
	rm -f initrd-%{ktag}-$kernel_flavour.img
fi
ln -sf initrd-%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}.img initrd-%{ktag}-$kernel_flavour.img
popd > /dev/null
%if %build_devel
if [ -d /usr/src/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel} ]; then
	ln -sf /usr/src/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel} /lib/modules/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}/build
	ln -sf /usr/src/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel} /lib/modules/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}/source
fi
%endif
EOF


### Create kernel Preun script on the fly
cat > $kernel_files-preun <<EOF
/sbin/installkernel -R %{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}
pushd /boot > /dev/null
if [ -L vmlinuz-%{ktag}-$kernel_flavour ]; then
	if [ "ls -l vmlinuz-%{ktag}-$kernel_flavour 2>/dev/null| awk '{ print $11 }'" = "vmlinuz-%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}" ]; then
		rm -f vmlinuz-%{ktag}-$kernel_flavour
	fi
fi
if [ -L initrd-%{ktag}-$kernel_flavour.img ]; then
	if [ "ls -l initrd-%{ktag}-$kernel_flavour.img 2>/dev/null| awk '{ print $11 }'" = "initrd-%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}.img" ]; then
		rm -f initrd-%{ktag}-$kernel_flavour.img
	fi
fi
popd > /dev/null
%if %build_devel
if [ -L /lib/modules/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}/build ]; then
	rm -f /lib/modules/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}/build
fi
if [ -L /lib/modules/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}/source ]; then
	rm -f /lib/modules/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}/source
fi
%endif
exit 0
EOF


### Create kernel Postun script on the fly
cat > $kernel_files-postun <<EOF
/sbin/kernel_remove_initrd %{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}
EOF
}


CreateKernel() {
	flavour=$1

	PrepareKernel $flavour %{ktag}-$flavour-%{buildrpmrel}

	BuildKernel %{kversion}-%{ktag}-$flavour-%{buildrpmrel}
	%if %build_devel
		SaveDevel $flavour
	%endif
	CreateFiles $flavour
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
%if %build_desktop586
CreateKernel desktop586
%endif
%endif

%if %build_desktop
CreateKernel desktop
%endif

%if %build_laptop
CreateKernel laptop
%endif

%if %build_server
CreateKernel server
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
for i in alpha arm arm26 avr32 blackfin cris frv h8300 ia64 mips m32r m68k m68knommu parisc powerpc ppc s390 sh sh64 v850 xtensa; do
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

### FIXME MDV bugs #29744, #29074, will be removed when fixed upstream
        mkdir -p %{target_source}/arch/s390/crypto/
        cp -fR arch/s390/crypto/Kconfig %{target_source}/arch/s390/crypto/

# other misc files
rm -f %{target_source}/{.config.old,.config.cmd,.mailmap,.missing-syscalls.d}

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
	/sbin/depmod -u -ae -b %{buildroot} -r -F %{target_boot}/System.map-$i $i
	echo $?
done

for i in *; do
	pushd $i
	echo "Creating module.description for $i"
	modules=`find . -name "*.ko.gz"`
	echo $modules | xargs /sbin/modinfo \
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
### source and doc file lists
###

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
### FIXME MDV bugs #29744, #29074, will be removed when fixed upstream
%{_kerneldir}/arch/s390
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

%files -n %{kname}-source-latest
%defattr(-,root,root)

%endif

%if %build_doc
%files -n %{kname}-doc-%{buildrel}
%defattr(-,root,root)
%doc linux-%{tar_ver}/Documentation/*
%endif

%changelog
* Mon Jun 25 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc6.1mdv
- update to kernel.org 2.6.22-rc6
- rediff patch AX10: High Resolution Timer Support & Tickless System 
- update patch CF01: Ingo Molnar's CFS-v18 Scheduler for 2.6.22-rc6

* Sun Jun 24 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc5.2mdv
- kernel-*-devel rpms does not provide kernel-source anymore
- jump the gun on smp-enabled kernels (to help main kernel transition),
  so every kernel is now smp enabled, and we rely on smp-alternatives
  to get it right on single processor/core systems
- drop "-smp" from kernel names, so now the only kernel flavours are:
  desktop586, desktop, laptop, server
- add obsoletes & provides to *-latest rpms to cope with the naming changes
- simplify specfile to match naming changes
- fix kernel descriptions & summarys to match the nanming changes
- re-add build & source symlinking logic to kernel-source rpm so
  it works with dkms
- update README.urpmi regarding theese changes
- update patch CF01: Ingo Molnar's CFS-v18 Scheduler
- update patch FS01: unionfs 2.0 v. linux-2.6.22-rc5-u1
- redo patch FS02: fix unionfs build with AppArmor
- update patch MB10: ndiswrapper 1.47
- update patch MB11: ndiswrapper Makefile fix
- update patch MC20: iwlwifi 0.0.32 and enable it
- drop patch MC21: iwlwifi include fix, merged upstream
- update defconfigs

* Sun Jun 17 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc5.1mdv
- update to kernel.org 2.6.22-rc5
- update patch AX10: High Resolution Timer Support & Tickless System 
  2.6.22-rc5-hrt1
- add patches DS01,DS02: Alsa pcspeaker support on ix86 (pkarlsen, #31058)
- disable CONFIG_SND_PCSP, still broken
- update patch FS01: unionfs 2.0 2.6.22-rc4-u1
- add patch FS02: fix unionfs build to work with AppArmor patchset
- update defconfigs

* Sat Jun 16 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc4.4mdv
- update patch AX10: High Resolution Timer Support & Tickless System
  2.6.22-rc4-hrt10
- update patch CF01: Ingo Molnar's CFS-v17 Scheduler
- drop patch CF02: merged upstream

* Wed Jun 13 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc4.3mdv
- macroized spec file is back (Thanks again Anssi)
- update patch AX10: High Resolution Timer Support & Tickless System
  2.6.22-rc4-hrt7
- drop patch CF02: SCHED_IDLEPRIO fix, fixed upstream
- add new patch CF02: CFS-v17-rc4

* Sun Jun 10 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc4.2mdv
- macroizing spec file, shortens it by ~1300 lines (BIG thanks goes
  to Anssi for providing the patch)
- fix macroizing to work with -smp flavour descriptions and summarys
- enable building of laptop(-smp) flavours for ix86 & x86_64 to start
  streamlining the defconfigs & optimizations
- update patch AX10: High Resolution Timer Support & Tickless System
  2.6.22-rc4-hrt6
- update patch CF01: Ingo Molnar's CFS-v16 Scheduler
- drop patch CF02: CFS smpboot mismerge fix, not needed anymore
- add new patch CF02: fix SCED_IDLEPRIO to actually be usable
- /sbin/modinfo-25 is now renamed to /sbin/modinfo
- SIGH... Revert macroizing spec file for now as the new rpm does
  not work with it, so it needs to be reworked :-(
- update defconfigs

* Tue Jun  5 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc4.1mdv
- update to kernel.org 2.6.22-rc4
- rediff patch AX10: High Resolution Timer Support & Tickless System
- rediff patch CF01: Ingo Molnar's CFS-v15 Scheduler
- add patch CF02: fix CFS smpboot mismerge on i386

* Mon Jun  4 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc3.2mdv
- update patch AX10: High Resolution Timer Support & Tickless System
  2.6.22-rc3-hrt2
- disable patches CK01-CK30: Con Kolivas 2.6.22-rc3-ck1 patchset
- add patch CF01: Ingo Molnar's CFS-v15 Scheduler (Request by Thierry)
- update patch MB40: acer_acpi 0.5 (requested by Ze)
- redo patch MB61: really fix ipw3945 Kconfig for 2.6.22-rc2+
- add patch MB72: fix rt2400 Kconfig for 2.6.22-rc2+
- add patch MB83: fix rt2500 Kconfig for 2.6.22-rc2+
- add patch MB91: fix rt2570 Kconfig for 2.6.22-rc2+
- add patch MC03: fix rt61 Kconfig for 2.6.22-rc2+
- add patch rt73: fix rt73 Kconfig for 2.6.22-rc2+
- enable CONFIG_SND_AC97_POWER_SAVE (requested by Austin)
- change from X86_BIGSMP to X86_GENERICARCH for ix86 smp config
- update defconfigs

* Wed May 30 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc3.1mdv
- update to kernel.org 2.6.22-rc3
- update patch AX10: High Resolution Timer Support & Tickless System
- update patches CK01-CK30: 2.6.22-rc3-ck1 patchset
- add patch MB22: add missng include linux/sched.h to fix squashfs build
- update patch MB60: ipw3945 1.2.1
- add patch MB61: fix ipw3945 Kconfig to work with 2.6.22+ series kernels
- drop patch CP01: cpu hotplug Kconfig depencies fix, shouldnt be needed anymore
- provide versioned kernel-devel and kernel-source (MDV #31006)

* Tue May 22 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc2.1mdv
- update to kernel.org 2.6.22-rc2
- add patch AX10: High Resolution Timer Support & Tickless System
  Support to x86_64 & Sparc64 (request by Thierry Vignaud)
- update patches CK01-CK30: Con Kolivas -ck patchset 2.6.22-rc2-ck1
- drop patch DA10: ati ixp700 support, merged upstream
- drop patches DI10, DI11: eth1394 autoload blocking, merged upstream
- add patch DN42: fix ipt_psd build
- add patch DN43: fix ipt_IFWLOG build
- drop patch DN50: dscape wireless stack, merged upstream
- rediff patch DV01: fbsplash support
- update patch FS01: unionfs 2.0: 2.6.22-rc2-u2
- update patch MB10: ndiswrapper 1.45-rc1
- add patch MB11: fix ndiswrapper srctree location
- add patch MB21: fix squashfs inode build
- update patches MC20, MC21: iwlwifi 0.0.18
- rediff patch NB01: bluetooth-alsa support
- update patches SA01-SA45: AppArmor 2.0.2-662
- drop patch SA50: missing security.h parameter, merged upstream
- remove blackfin arch files
- disable CONFIG_IRQBALANCE on i386-smp, in favour of the better
  working userspace irqbalance daemon from contribs (Requested by Austin)
- disable a few options:
  * IP_NF_SET: needs more fixes to work with 2.6.22-rc2+ kernels
  * UNION_FS: needs to be adapted for AppArmor
  * IWLWIFI: need to be adapted for 2.6.22-rc2+ kernels
- update defconfigs

* Fri May 18 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21.1-2mdv
- gzip kernel (and thereby rename it consistently to vmlinuz) 
  on sparc too (peroyvind)
- add patch CK24: Swap Prefetch bugfixes and optimizations,
  brings the code to 2.6.21-ck2 level (Con Kolivas)
- redo patch DA10: change it to full ATI IXP700 support:
  * IDE, PATA, SATA, AHCI, I2C, SMBUS
- add patch SA50: fix include/linux/security.h missing parameter,
  needed on sparc builds (peroyvind, #30700)
- enable CONFIG_TIMER_STATS (request by Michael Braun)
- update kernel-tmb-source description to point out:
  * only needed when building own kernels
  * othervise install a mztching -devel- rpm
- /sbin/depmod-25 is now renamed to /sbin/depmod
  
* Sun May  6 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21.1-1mdv
- update to kernel.org 2.6.21.1:
  * IPV6: Fix for RT0 header ipv6 change
  * IPV4: Fix OOPS'er added to netlink fib
- add patch AI03: picopower irq router fix, found when merged into
  kernel.org -mm series (Andrew Morton)
- drop patch CK00: standalone SD scheduler v. 0.46
- update patches CK01-CK23: Cons CK patchset 2.6.21-ck1,
  now built around with the new SD scheduler v. 0.48 as base
- add patch CK30: add Kconfig option to switch between -ck (desktop),
  and -cks (server) oriented optimizations of the CK patchset
- add patch DA10: adds support for ATI IXP700 SATA & AHCI
- update defconfigs
- update README.urpmi regarding kernel-tmb-source

* Fri Apr 27 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-2mdv
- revert read-only -devel rpms until I find a better solution...

* Thu Apr 26 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-1mdv
- update to kernel.org 2.6.21 final
- drop patch AA00: 2.6.21-rc7-git6, merged upstream
- make devel trees read-only (like in kernel-multimedia series),
  to try and work around broken dkms & co
- add /arch/s390/crypto/Kconfig to -devel and -source trees, fixes 
  MDV bugs #29744, #29074 (reported against kernel-linus, but affects 
  all post 2.6.20-rc3 series kernels, will be removed if/when fixed upstream

* Wed Apr 25 2007 Thomas Backlund <tmb@mandriva.org> 2.6.21-0.rc7.1mdv
- fix patches tarball -rc versioning
- update to kernel.org 2.6.21-rc7
- add patch AA00: 2.6.21-rc7-git6
- rediff patch AS01: linux-phc support
- drop patch AX02: nmi watchdog timeout fix, merged upstream
- update patch CE02: acpi-dsdt-initrd v0.8.4
- update patch CK00: to SD sceduler v0.46 for 2.6.21 series
- update patches CK01-CK24: Con Kolivas 2.6.21-rc7-ck2 patchset
- rediff patch CR01: badram support
- drop patch DA01: acpi update, merged upstream
- drop patch DB01: bluetooth update, merged upstream
- drop patches DC01-DC05: agpgart 1.0.2, merged upstream
- drop patch DC10: drm update, merged upstream
- drop patch DM10: mmc update, merged upstream
- drop patch DM20: tifm update, merged upstream
- drop patch DN03: bcm43xx speed fix, fixed differently upstream
- add patch DN41: fixes netfilter IFWLOG, PSD, SET builds
- update patch DN50: mac80211 v.7.0.6 (dscape stack)
- drop patch DS01: alsa update, merged upstream
- drop patch DU01: usb-rndis-lite, merged upstream
- rediff patch DV01: fbsplash support
- update patch FS01: unionfs 2.0 to 2.6.21-rc7-u1
- drop patches FS11-FS13: supermount support
- update patch MB30: acerhk 0.5.35
- update patch MB40: acer_acpi 0.4
- update patch MC20: iwlwifi 0.0.13
- add patch MC21: fix iwlwifi includes
- drop patches SA01-SA06: Apparmor v288
- add patches SA01-SA41: Apparmor v564
- update defconfigs

* Mon Apr 23 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.7-5mdv
- update patch CK00: SD scheduler v 0.46

* Sat Apr 21 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.7-4mdv
- update patch CK00: SD scheduler v 0.44

* Thu Apr 19 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.7-3mdv
- update patch CK00: SD scheduler v 0.42 and re-enable it
- disable patches CK01-CK11,CK21,CK30: old Staircase Scheduler,
  as SD sceduler is not dead after all...

* Wed Apr 18 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.7-2mdv
- disable patch CK00: SD Scheduler as Con decided to drop the development
- re-enable patches CK01-CK11,CK21,CK30: Staircase scheduler v17,
  as Con decided to return it as the base for the -ck sets again
- add patch DU01: update usb-rndis-lite to support wm5 (#30130, #30128)
- update patch MB10: ndiswrapper 1.42
- add patch NB10: add sco-flowcontrol support to bluetooth, needed for
  bluetooth-alsa (Requested by Guillaume Bedot)
- update defconfigs

* Sun Apr 15 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.7-1mdv
- update to kernel.org 2.6.20.7:
  -  http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.20.7
- drop patch AA00: merged upstream
- add patch AI02: add support for picopower Irq router (Requested by Austin)
- update patch CK00: SD scheduler 0.40
  
* Thu Apr 12 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.6-3mdv
- add patch AA00: 2.6.20.7-rc1
- drop patch AA01-AA06, DA20: merged upstream

* Sun Apr 08 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.6-2mdv
- enable CONFIG_AUDIT and CONFIG_AUDITSYSCALL, used by pam
- add patches from Stefan Richter (kernel.org ieee1394 maintainer)(#20126)
    DI10_382b-ieee1394-eth1394-dont-autoload-by-hotplug-when-ohci1394-starts.patch
    DI11_392b-ieee1394-nodemgr-less-noise-in-dmesg.patch
- add drivers/md/dm.h to -devel packages, needed for truecrypt build (Danny)
- update patch MB10: ndiswrapper 1.41
- update defconfigs

* Sat Apr 07 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.6-1mdv
- update to kernel.org 2.6.20.6:
  - fixes CVE-2007-1357, and other bugfixes:
    - http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.20.6
    - http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.20.5
- drop patches AA00,AA02,AA03: merged upstream

* Thu Apr 05 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.4-4mdv
- add patches AA00-AA06: 2.6.20.5-rc1 + fixes
- add patch AX02: increase NMI watchdog timeout for Quad Core Opterons
- update patch CK00: Staircase-Deadline scheduler to 0.39
- add patch DA20: fix SB600 sata h/w internal error
- fix unistall scripts (#30048)

* Wed Mar 27 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.4-3mdv
- update patch CK00: Staircase-Deadline scheduler 0.37

* Wed Mar 27 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.4-2mdv
- update patch CK00: Staircase-Deadline scheduler 0.36

* Sat Mar 24 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.4-1mdv
- update to kernel.org: 2.6.20.4
    http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.20.4
- update patch CK00: RSDL scheduler 0.33
- rediff patch CK22

* Sun Mar 18 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.3-2mdv
- update patch CK00: RSDL scheduler to 0.31

* Tue Mar 13 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.3-1mdv
- update to kernel.org 2.6.20.3
- drop patches AA01-AA20: merged upstream

* Mon Mar 12 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.2-3mdv
- update patch CK00: RSDL scheduler to 0.30

* Sun Mar 11 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.2-2mdv
- update patch CK00: rsdl scheduler to 0.29
- add patch DN16: nozomi debug and oops at unload fix (from main)
- update patch MB10: ndiswrapper 1.38

* Sat Mar 10 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.2-1mdv
- update to kernel.org 2.6.20.2
  fixes: CVE-2007-1000, CVE-2007-0005, other fixes:
  http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.20.2
- drop patches AA01-AA06: merged upstream
- add new patches AA01-AA20: 2.6.20.3-rc1
- rewrite spec once more ;-)
  use cat & eof instead of echo to create scripts and files on the fly,
  makes the spec more readable (suggested by Danny)
  merge the rest of scripts
- re-add sparc64 support, and actually make it work this time
- add patch AX01: fix data corruption on-nVidia chipsets and ide/sata
- update patch CK00: update RSDL scheduler to 0.28
- drop patch DC03: merged upstream
- update patch DC10: drm to 2.6.21-rc3
- drop patch DM01: merged upstream
- add patch DM10: update mmc support to 2.6.21-rc3 level
- add patch DM20: update tifm_7xx1 to v 0.7 (AdamW request)
- rediff patch DS01: alsa-1.0.14rc3

* Tue Mar 06 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.1-4mdv
- rename kernel-headers-* packages to more appropriate kernel-devel-*
- have *-devel-latest obsolete *-headers-latest
- drop requires between kernel-*-devel and kernel-*
- install devel files in /usr/src/'uname -r'
- install full source in /usr/src/<version>-tmb-<release>
- create post/postun/preun scripts at build time (removes code duplication)
- update README.urpmi
- configure server kernels to use CFQ i/o sceduler by default too
- update patch CK00: Con Kolivas rotating staircase deadline scheduler 
  to v. 0.26 and re-enable it, as it's now stable
- disable patches CK01-CK11, CK21, CK30: old Staircase v17 scheduler
- add patch DB01: bluetooth v. 1.2 (#29169) 
- add patch DC10: update drm to 2.6.21-rc2-git4
- rollback patch DN50: dscape stack to v1.0.0 for now as the newer ones
  breaks the stable kernel.org drivers.
- disable patch DN51: wireless.git update for now as it needs the newer
  dscape stack
- rollback patch MC20: iwlwifi to 0.0.8 as the newer code depends on
  newer dscape stack

* Mon Feb 26 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.1-3mdv
- add patch AS01: Linux Processor Hardware Control v.0.2.9 (Josh Schneider)
- update patch DN50: dscape wireless stack to 3.0.2
- add patch DN51: wireless.git 20070225: drivers using the dscape stack:
  adm8211, bcm43xx, prism54, rt2400, rt2500, rt61, rt73, zd1211
- update patch DS01: alsa 1.0.14rc3 (tvignaud request)
- drop patch FQ01: cpufreq-speedstep-dothan-3 (merged in patch AS01)
- enable CONFIG_CC_OPTIMIZE_FOR_SIZE (tvignaud request)
- update patch MC20: iwlwifi to 0.0.9
- update defconfigs
- post script fixes

* Fri Feb 23 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.1-2mdv
- really fix build and source symlinks for desktop586 series (#28843)
- add patch DN03: fix Broadcom 4311, 4312 detection (#28878)

* Wed Feb 21 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.1-1mdv
- update to kernel.org 2.6.20.1:
  - Fix a free-wrong-pointer bug in nfs/acl server (CVE-2007-0772)
- fix header paths in desktop-i586(-smp) rpms (#28843)
- fix missing arch/i386/kernel/sigframe.h in header rpms (#28843)
- update patch MC20: iwlwifi to v 0.0.8

* Sun Feb 18 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20-4mdv
- fix RC versioning
- fix the whole autoconf mess
    dont rely on /etc/init.d/kheader and /boot/kernel.h anymore
    drop all of the old autoconf hacks
    drop kernel-tmb-source-stripped(-latest) rpms
    introduce kernel-tmb-$flavour-headers(-latest) rpms to build 3rdparty 
    drivers against (survives test: make mrproper oldconfig prepare scripts)
    kernel-tmb-source rpm does not include any autoconf stuff anymore
    add info regarding this to README.urpmi
- add patch AA01: fix-missing-critical-phys_to_virt-in-lib_swiotlb
- add patch AA02: ieee1394-video1394-DMA-fix
- add patch AA03: ieee1394-fix-host-device-registering-when-nodemgr-disabled
- add patch AA04: fix-oops-in-xfrm_audit_log
- add patch AA05: md-raid5-fix-crash
- add patch AA06: md-raid5-fix-export-blk_recount_segments
- update patch CK00: Con Kolivas rotating staircase deadline scheduler 0.17,
  but disable it for now, as it's still buggy according to Con.
- update patches CK01-CK23: Con Colivas 2.6.20-ck1 patchset, and
  re-enable patches CK01-CK11, CK21: Staircase v17 scheduler, as the
  kernel freeze bug has been found and fixed.
- add patch CK30 : add ck_server_tuned config option and server optimization.
- add patch DM01: fix cx25840 firmware loading (Stefan van der Eijk)
- update patch MB10: ndiswrapper to 1.37
- add patch MB31: acerhk include fix
- redo patch MB52: qc-usb include fix
- add patch MB82: rt2500 include fix
- update patch MB20: squashfs 3.2-r2
- drop patch MB21: squashfs build fix, merged upstream

* Sun Feb 11 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20-3mdv
- update patch CK00: rotating staircase deadline scheduler 0.14
- add patches DC01-DC05: agpgart 1.0.2 (request by Colin Guthrie)
- add patch DN50: dscape ieee802.11 wireless network stack
- update patch MB50: qc-usb to 0.6.5
- drop patch MB52: qc-usb include fix (merged upstream)
- add patches MC20: Intel opensource 3945 wireless driver 0.0.5
    - info and firmware at http://intellinuxwireless.org/
- update defconfigs

* Tue Feb  6 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20-2mdv
- update patches CK01-CK23: Con Kolivas patchset 2.6.20-rc6-ck1
- disable patches CK01-CK11, CK21: old staircase scheduler
- add patch CK00: Con Kolivas new rotating staircase deadline cpu scheduler 0.11
- update pach FS01: unionfs to v 2.0
- drop patches FS02, FS03: unionfs buildfixes (not needed anymore)
- rediff patch FS11,FS13: supermount

* Mon Feb  5 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20-1mdv
- update to kernel.org 2.6.20 final
- drop patch AA01: merged upstream

* Sun Feb  4 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.0.rc7-3mdv
- update patch AA01: to 2.6.20-rc7-git4

* Fri Feb  2 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.0.rc7-2mdv
- add patch AA01: 2.6.20-rc7-git1
- add patch DA01: acpi 20070126
- update patch DN15: nozomi driver from GregKH / 2.6.20-rc6-mm3
- update defconfigs

* Thu Feb  1 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.0.rc7-1mdv
- update to kernel.org: 2.6.20-rc7
- drop patch CP02: P4 clockmon N60 errata fix (not needed anymore)
- rediff patch DS01: alsa 1.0.14rc2
- merge patches from main kernel:
  - add patch MB70-MB71: RaLink RT2400 series wireless chipset support
  - add patch MB80-MB81: RaLink RT2500 series wireless chipset support
  - add patch MB90: RaLink RT2570 series USB Wireless chipset support
  - add patches MC00-MC02: RaLink RT2561 & RT2661 PCI Wireless chipset support
  - add patches MC10-MC12: RaLink RT2571 & RT2671 series USB Wireless chipset
- update defconfigs

* Sat Jan 27 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.0.rc6-2mdv
- add patch MB60: ipw3945 v 1.2.0
- fix missing / in post scripts (reported by Dick Gevers)
- update defconfigs

* Thu Jan 25 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.0.rc6-1mdv
- update to kernel.org: 2.6.20-rc6
- drop patch AA01: profile_hits export (merged upstream)
- rediff patch DS01: alsa 1.0.14rc2
- update defconfigs

* Thu Jan 25 2007 Thomas Backlund <tmb@mandriva.org> 2.6.20.0.rc5-1mdv
- update to kernel.org: 2.6.20-rc5
- add patch AA01: fix export of profile_hits, needed for KVM on UP 
- update patches CK01-CK26 to CK01-CK22: Con Kolivas 2.6.20-rc5-ck1
- rediff patch CE02: acpi dsdt initrd support
- rediff patch CR01: BadRAM support
- rediff patch DA02: fix acpi double proc video entry
- rediff patch DM02: dmraid45 support
- add patch DM03: fix dmraid4-5 build for 2.6.20
- drop patch DN10: ipw2200 v1.2.0 (merged upstream)
- add patch DN37: netfilter IFWLOG buildfix for 2.6.20
- add patch DS01: alsa 1.0.14rc2
- drop patch DS03: asus w6a quirk (merged upstream)
- rediff DV01: fbsplash support for 2.6.20
- update patch FS01: unionfs support to 1.5pre-cvs200701171418
- add patch FS02: unionfs build fix for 2.6.20
- drop patch FS10: inode oops fix (not needed anymore)
- rediff patch FS11: supermount 2.0.4 support
- rediff patch FS13: supermount 2.0.5 update
- update patch MB10: ndiswrapper to 1.35-rc1
- add patch MB21: squashfs build fix for 2.6.20
- update patches SA01-SA04: AppArmor v288
- add patch SA06: apparmor buildfix for 2.6.20
- update defconfigs
- disable dmraid4-5 support for now as it's broken...

* Sun Jan 21 2007 Thomas Backlund <tmb@mandriva.org> 2.6.19.2-3mdv
- update README.urpmi regarding modular ide and other partitions
- update patch CR01: BadRAM to 2.6.19.1 level (David Walser)
- drop patch DB16: gzloop, not used anymore (Oliver Blin)
- fix "static" symlinks in /boot when it's on sepatate partition
- remove "static" symlinks if last kernel-tmb is uninstalled

* Sat Jan 13 2007 Thomas Backlund <tmb@mandriva.org> 2.6.19.2-2mdv
- update patch MB20: squashfs to v3.2
- drop patch MB21: not needed anymore
- update patch FS01: unionfs to 1.5pre-cvs200701042308, and enable it

* Wed Jan 10 2007 Thomas Backlund <tmb@mandriva.org> 2.6.19.2-1mdv
- update to kernel.org 2.6.19.2:
    - bonding: incorrect bonding state reported via ioctl
    - dvb-core: fix bug in CRC-32 checking on 64-bit systems
    - x86-64: Mark rdtsc as sync only for netburst, not for core2
    - Fix for shmem_truncate_range() BUG_ON()
    - ebtables: don't compute gap before checking struct type
    - asix: Fix typo for AX88772 PHY Selection
    - IPV4/IPV6: Fix inet{,6} device initialization order
    - UDP: Fix reversed logic in udp_get_port()
    - SPARC64: Fix "mem=xxx" handling
    - SPARC64: Handle ISA devices with no 'regs' property
    - SOUND: Sparc CS4231: Use 64 for period_bytes_min
    - NET: Don't export linux/random.h outside __KERNEL__
    - ramfs breaks without CONFIG_BLOCK
    - i2c: fix broken ds1337 initialization
    - fix aoe without scatter-gather [Bug 7662]
    - handle ext3 directory corruption better (CVE-2006-6053)
    - ext2: skip pages past number of blocks in ext2_find_entry (CVE-2006-6054)
    - connector: some fixes for ia64 unaligned access errors
    - SOUND: Sparc CS4231: Fix IRQ return value and initialization
    - V4L: Fix broken TUNER_LG_NTSC_TAPE radio support
    - V4L: cx2341x: audio_properties is an u16, not u8
    - dm-crypt: Select CRYPTO_CBC
    - sha512: Fix sha384 block size
    - read_zero_pagealigned() locking fix
    - fix OOM killing of swapoff
    - sched: fix bad missed wakeups in the i386, x86_64, ia64, ACPI and APM idle code
    - sparc32: add offset in pci_map_sg()
    - V4L: cx88: Fix leadtek_eeprom tagging
    - Revert "zd1211rw: Removed unneeded packed attributes
    - VM: Fix nasty and subtle race in shared mmap'ed page writeback
    - Fix incorrect user space access locking in mincore() (CVE-2006-4814)
    - Bluetooth: Add packet size checks for CAPI messages (CVE-2006-6106)
    - DVB: lgdt330x: fix signal / lock status detection bug
    - cciss: fix XFER_READ/XFER_WRITE in do_cciss_request
    - NetLabel: correctly fill in unused CIPSOv4 level and category mappings
    - Fix up page_mkclean_one(): virtual caches, s390
    - corrupted cramfs filesystems cause kernel oops (CVE-2006-5823)
    - PKTGEN: Fix module load/unload races
    - IB/srp: Fix FMR mapping for 32-bit kernels and addresses above 4G
    - kbuild: don't put temp files in source
    - ARM: Add sys_*at syscalls
    - Buglet in vmscan.c
    - i386: CPU hotplug broken with 2GB VMSPLIT
    - ieee1394: ohci1394: add PPC_PMAC platform code to driver probe
    - libata: handle 0xff status properly
    - SCSI: add missing cdb clearing in scsi_execute()
    - sched: remove __cpuinitdata anotation to cpu_isolated_ma
    - ieee80211softmac: Fix mutex_lock at exit of ieee80211_softmac_get_genie
    - softmac: Fixed handling of deassociation from AP
    - zd1211rw: Call ieee80211_rx in tasklet
    - smc911x: fix netpoll compilation faliure
- drop patch AA02: merged upstream
- drop patch FS20: merged upstream
- remove support for sparc (32 bit)
- add info to README.urpmi regarding modular ide and PATA CD/DVD

* Sun Dec 31 2006 Thomas Backlund <tmb@mandriva.org> 2.6.19.1-4mdv
- drop patch FS13: old supermount fix
- add patch FS13: update supermount to 2.0.5 (Andrey Borzenkov) (#27665)
- add patch FS20: really fix file content corruption (#27693, #27859)

* Thu Dec 21 2006 Thomas Backlund <tmb@mandriva.org> 2.6.19.1-3mdv
- add support for static boot entries using symlinks in /boot
- drop patch FS20: content corruption fix, does not fix the problem

* Tue Dec 17 2006 Thomas Backlund <tmb@mandriva.org> 2.6.19.1-2mdv
- add patch MB21: fix squashfs build and re-enable it
- update patch FS13: supermount buildfix
- disable supermount as it still oopses
- enable ecryptfs
- add patch FS20: try to fix file content corruption (from LKML) (#27693)
- really disable supermount

* Tue Dec 12 2006 Thomas Backlund <tmb@mandriva.org> 2.6.19.1-1mdv
- update to kernel.org 2.6.19.1:
    - NETLINK: Put {IFA,IFLA}_{RTA,PAYLOAD} macros back for userspace
    - forcedeth: Disable INTx when enabling MSI in forcedeth
    - x86: Fix boot hang due to nmi watchdog init code
    - m32r: make userspace headers platform-independent
    - softirq: remove BUG_ONs which can incorrectly trigger
    - autofs: fix error code path in autofs_fill_sb()
    - PM: Fix swsusp debug mode testproc
    - compat: skip data conversion in compat_sys_mount when data_page is NULL
    - drm-sis linkage fix
    - add bottom_half.h
    - NETLINK: Restore API compatibility of address and neighbour bits
    - IrDA: Incorrect TTP header reservation
    - IPSEC: Fix inetpeer leak in ipv4 xfrm dst entries
    - USB: Fix oops in PhidgetServo
    - XFRM: Use output device disable_xfrm for forwarded packets
    - TOKENRING: Remote memory corruptor in ibmtr.c
    - do_coredump() and not stopping rewrite attacks? (CVE-2006-6304)
    - IB/ucm: Fix deadlock in cleanup
    - softmac: fix unbalanced mutex_lock/unlock in ieee80211softmac_wx_set_mlme
    - NETFILTER: bridge netfilter: deal with martians correctly
    - NETFILTER: Fix iptables compat hook validation
    - NETFILTER: Fix {ip, ip6, arp}_tables hook validation
    - SUNHME: Fix for sunhme failures on x86
    - PKT_SCHED act_gact: division by zero
    - Revert "ACPI: SCI interrupt source override"
    - cryptoloop: Select CRYPTO_CBC
    - NET_SCHED: policer: restore compatibility with old iproute binaries
    - EBTABLES: Prevent wraparounds in checks for entry components' sizes
    - EBTABLES: Deal with the worst-case behaviour in loop checks
    - EBTABLES: Verify that ebt_entries have zero ->distinguisher
    - EBTABLES: Fix wraparounds in ebt_entries verification
    - softmac: remove netif_tx_disable when scanning
    - IPV6 NDISC: Calculate packet length correctly for allocation
- drop patches AA01,AA03: merged upstream
- add patch FS13: fix supermount build on 2.6.19

* Sun Dec 10 2006 Thomas Backlund <tmb@mandriva.org> 2.6.19-4mdv
- bump release to get it past the buildsystem

* Sat Dec  9 2006 Thomas Backlund <tmb@mandriva.org> 2.6.19-3mdv
- fix include/linux/config.h install point
- fix mismerged patch DM02: dm-raid45 support

* Sat Dec  9 2006 Thomas Backlund <tmb@mandriva.org> 2.6.19-2mdv
- readd include/linux/config.h until the autoconf stuff is reworked
- update patch MB10: ndiswrapper to 1.31
- drop patch 100: merged in upcoming 2.6.19.1
- add patch AA01: 2.6.19.1-rc2
- add patch AA02: DM_CRYPT needs CRYPTO_CBC
- add patch AA03: add missing bottom_half.h from 2.6.19.1-rc2
- update patches CK01-CK26: Con Colivas 2.6.19-ck2

* Wed Dec  6 2006 Thomas Backlund <tmb@mandriva.org> 2.6.19-1mdv
- update to kernel.org 2.6.19
- update patches CK01-CK25: Con Colivas CK1 patchset
- drop patch AX01_fix-x86_64-linking-on-32bit (merged upstream)
- drop patch DC01_add_via_drm_pciid (merged upstream)
- drop patch DF01_generic_acl_structure (merged upstream)
- drop patch DF02_add_acl_to_tmpfs (merged upstream)
- drop patch DI08_libata_enable (merged upstream)
- disable patch DM01: enable_broken_dmstripe (shouldn't be needed anymore)
- rediff patch DM02: dm-raid45 support
- drop patch DN06: e100 v 3.5.14 (newer version upstream)
- rediff patch DN10: ipw2200 v 1.2.0
- add patch: DN35_ipset_needs_listhelp until ipser is reworked for 2.6.19
- drop patch DP03_ICH7-8_quirks (merged upstream)
- disable patch DS02_alsa_hda-intel-error-handling (may not be needed anymore)
- rediff patch DV01: fbsplash-0.9.2-r5
- drop patch DV25_intel_agp_965 (merged upstream)
- drop patch DV26_i965_drm_support (merged upstream)
- rediff patch FS01: unionfs 1.4.0
- rediff patch MB02: 3rdparty merge
- add patch: MB53_qc-usb-includes2: fixes build
- add patch: SA05_fix_apparmor_inline_build: fixes build
- update defconfigs for 2.6.19 series
- add patch100: revert ACPI_SCI_interrupt_source_override, will be removed
  when 2.6.19.1 is released...
  
* Sat Dec  2 2006 Thomas Backlund <tmb@mandriva.org> 2.6.18.5-1mdv
- update to kernel.org 2.6.18.5:
    - pcmcia: fix 'rmmod pcmcia' with unbound devices
    - BLUETOOTH: Fix unaligned access in hci_send_to_sock
    - alpha: Fix ALPHA_EV56 dependencies typo
    - TG3: Add missing unlock in tg3_open() error path
    - softmac: fix a slab corruption in WEP restricted key association
    - AGP: Allocate AGP pages with GFP_DMA32 by default
    - V4L: Do not enable VIDEO_V4L2 unconditionally
    - bcm43xx: Drain TX status before starting IRQs
    - fuse: fix Oops in lookup
    - UDP: Make udp_encap_rcv use pskb_may_pull
    - NETFILTER: Missing check for CAP_NET_ADMIN in iptables compat layer
    - NETFILTER: ip_tables: compat error way cleanup
    - NETFILTER: ip_tables: fix module refcount leaks in compat error paths
    - NETFILTER: Missed and reordered checks in {arp,ip,ip6}_tables
    - NETFILTER: arp_tables: missing unregistration on module unload
    - NETFILTER: Honour source routing for LVS-NAT
    - NETFILTER: Kconfig: fix xt_physdev dependencies
    - NETFILTER: xt_CONNSECMARK: fix Kconfig dependencies
    - NETFILTER: H.323 conntrack: fix crash with CONFIG_IP_NF_CT_ACCT
    - IA64: bte_unaligned_copy() transfers one extra cache line
    - x86 microcode: don't check the size
    - scsi: clear garbage after CDBs on SG_IO
    - IPV6: Fix address/interface handling in UDP and DCCP, according to the scoping architecture
    
* Fri Dec  1 2006 Thomas Backlund <tmb@mandriva.org> 2.6.18.4-1mdv
- update to kernel.org 2.6.18.4:
    - bridge: fix possible overflow in get_fdb_entries (CVE-2006-5751)
    
* Tue Nov 21 2006 Thomas Backlund <tmb@mandriva.org> 2.6.18.3-2mdv2007.1
- redo patch DN10: update ipw2200 to 1.2.0
- re-enable ipw2200 in defconfigs

* Sun Nov 19 2006 Thomas Backlund <tmb@mandriva.org> 2.6.18.3-1mdv2007.1
- update to 2.6.18.3
    - CIFS: New POSIX locking code not setting rc properly to zero on successful
    - CIFS: report rename failure when target file is locked by Windows
    - cciss: fix iostat
    - cpqarray: fix iostat
    - Char: isicom, fix close bug
    - block: Fix bad data direction in SG_IO
    - pci: don't try to remove sysfs files before they are setup
    - Patch for nvidia divide by zero error for 7600 pci-express card
    - CPUFREQ: Make acpi-cpufreq unsticky again
    - security/seclvl.c: fix time wrap (CVE-2005-4352)
    - fix via586 irq routing for pirq 5
    - NET: Set truesize in pskb_copy
    - TCP: Don't use highmem in tcp hash size calculation
    - correct keymapping on Powerbook built-in USB ISO keyboards
    - x86_64: Fix FPU corruption
    - Input: psmouse - fix attribute access on 64-bit systems
    - NET: __alloc_pages() failures reported due to fragmentation
    - e1000: Fix regression: garbled stats and irq allocation during swsusp
    - usbtouchscreen: use endpoint address from endpoint descriptor
    - USB: failure in usblp's error path
    - init_reap_node() initialization fix
    - ipmi_si_intf.c sets bad class_mask with PCI_DEVICE_CLASS
    - fix UFS superblock alignment issues
    - SPARC: Fix missed bump of NR_SYSCALLS
    - Fix sys_move_pages when a NULL node list is passed
    - SPARC64: Fix futex_atomic_cmpxchg_inatomic implementation
    - POWERPC: Make alignment exception always check exception table
    - S390: user readable uninitialised kernel memory, take 2
- add patch DB16: add support for gzloop

* Wed Nov 15 2006 Thomas Backlund <tmb@mandriva.org> 2.6.18.2-3mdv2007.1
- add patches SA01-SA04: Novell AppArmor v154
- update defconfigs to enable Security Capabilities and AppArmor 

* Mon Nov 13 2006 Thomas Backlund <tmb@mandriva.org> 2.6.18.2-2mdv2007.1
- bump release
- disable nozomi build

* Mon Nov  6 2006 Thomas Backlund <tmb@mandriva.org> 2.6.18.2-1mdv2007.0
- update to kernel.org 2.6.18.2
    - usbfs: private mutex for open, release, and remove
    - md: check bio address after mapping through partitions
    - IPV6: fix lockup via /proc/net/ip6_flowlabel [CVE-2006-5619]
    - tcp: cubic scaling error
    - JMB 368 PATA detection
    - fill_tgid: fix task_struct leak and possible oops
    - Use min of two prio settings in calculating distress for reclaim
    - vmscan: Fix temp_priority race
    - NFS: nfs_lookup - don't hash dentry when optimising away the lookup
    - Reintroduce NODES_SPAN_OTHER_NODES for powerpc
    - PCI: Remove quirk_via_abnormal_poweroff
    - SPARC64: Fix PCI memory space root resource on Hummingbird
    - ISDN: fix drivers, by handling errors thrown by ->readstat()
    - ISDN: check for userspace copy faults
    - rtc-max6902: month conversion fix
    - posix-cpu-timers: prevent signal delivery starvation
    - fix Intel RNG detection
    - Watchdog: sc1200wdt - fix missing pnp_unregister_driver()
    - ALSA: snd_rtctimer: handle RTC interrupts with a tasklet
    - uml: remove warnings added by previous -stable patch
    - uml: make Uml compile on FC6 kernel headers
    - x86-64: Fix C3 timer test
    - SCTP: Always linearise packet on input
    - NET: Fix skb_segment() handling of fully linear SKBs
    - fix missing ifdefs in syscall classes hookup for generic targets
    - SCSI: aic7xxx: pause sequencer before touching SBLKCTL
    - sky2: 88E803X transmit lockup (2.6.18)
    - Fix potential interrupts during alternative patching
    - fuse: fix hang on SMP
    - IB/mthca: Use mmiowb after doorbell ring
    - IPoIB: Rejoin all multicast groups after a port event
    - SCSI: aic7xxx: avoid checking SBLKCTL register for certain cards
    - knfsd: Fix race that can disable NFS server
    - md: Fix calculation of ->degraded for multipath and raid10
    - md: Fix bug where spares don't always get rebuilt properly when they become live
    - ALSA: Fix re-use of va_list
    - DVB: fix dvb_pll_attach for mt352/zl10353 in cx88-dvb, and nxt200x
    - bcm43xx: fix watchdog timeouts
    - SPARC64: Fix memory corruption in pci_4u_free_consistent()
    - SPARC64: Fix central/FHC bus handling on Ex000 systems
    - JFS: pageno needs to be long
    - Bluetooth: Check if DLC is still attached to the TTY
    - SERIAL: Fix oops when removing suspended serial port
    - SERIAL: Fix resume handling bug
    - Fix uninitialised spinlock in via-pmu-backlight code
    - SCSI: DAC960: PCI id table fixup
    - uml: fix processor selection to exclude unsupported processors and features
    - sky2: GMAC pause frame
    - sky2: accept multicast pause frames
    - ALSA: Repair snd-usb-usx2y for usb 2.6.18
    - ALSA: Fix bug in snd-usb-usx2y's usX2Y_pcms_lock_check()
    - ALSA: Dereference after free in snd_hwdep_release()
    - sound/pci/au88x0/au88x0.c: ioremap balanced with iounmap
    - ALSA: powermac - Fix Oops when conflicting with aoa driver
    - ALSA: emu10k1: Fix outl() in snd_emu10k1_resume_regs()
    - sky2: turn off PHY IRQ on shutdown
    - sky2: pause parameter adjustment
    - sky2: MSI test race and message
    - mm: fix a race condition under SMC + COW
    - __div64_32 for 31 bit
    - splice: fix pipe_to_file() ->prepare_write() error path
    - Fix sfuzz hanging on 2.6.18
- replace patch CK01 with CK01-CK24: Con Colivas patchset with the 
  broken-out versions to make it easier to disable some parts
- disable patch CK18: mm-prio_dependant_scan-1 as it conflicts with the
  chnges in the stable .2
- rediff patches CK14, CK15, CK23
- update patch FS01: unionfs to 1.4  

* Mon Oct 23 2006 Thomas Backlund <tmb@mandriva.org> 2.6.18.1-1mdv2007.0
- update to kernel.org 2.6.18.1
    - add utsrelease.h to the dontdiff file
    - V4L: copy-paste bug in videodev.c
    - block layer: elv_iosched_show should get elv_list_lock
    - NETFILTER: NAT: fix NOTRACK checksum handling
    - bcm43xx: fix regressions in 2.6.18
    - x86-64: Calgary IOMMU: Fix off by one when calculating register space location
    - ide-generic: jmicron fix
    - scx200_hrt: fix precedence bug manifesting as 27x clock in 1 MHz mode
    - invalidate_inode_pages2(): ignore page refcounts
    - rtc driver rtc-pcf8563 century bit inversed
    - fbdev: correct buffer size limit in fbmem_read_proc()
    - mm: bug in set_page_dirty_buffers
    - TCP: Fix and simplify microsecond rtt sampling
    - MD: Fix problem where hot-added drives are not resynced
    - IPV6: Disable SG for GSO unless we have checksum
    - PKT_SCHED: cls_basic: Use unsigned int when generating handle
    - sata_mv: fix oops
    - SPARC64: Fix sparc64 ramdisk handling
    - IPV6: bh_lock_sock_nested on tcp_v6_rcv
    - CPUFREQ: Fix some more CPU hotplug locking
    - SPARC64: Fix serious bug in sched_clock() on sparc64
    - Fix VIDIOC_ENUMSTD bug
    - load_module: no BUG if module_subsys uninitialized
    - i386: fix flat mode numa on a real numa system
    - cpu to node relationship fixup: map cpu to node
    - cpu to node relationship fixup: acpi_map_cpu2node
    - backlight: fix oops in __mutex_lock_slowpath during head /sys/class/graphics/fb0/*
    - do not free non slab allocated per_cpu_pageset
    - rtc: lockdep fix/workaround
    - i386 bootioremap / kexec fix
    - powerpc: Fix ohare IDE irq workaround on old powermac
    - sysfs: remove duplicated dput in sysfs_update_file
    - powerpc: fix building gdb against asm/ptrace.h
    - Remove offsetof() from user-visible <linux/stddef.h>
    - Clean up exported headers on CRIS
    - Fix v850 exported headers
    - Don't advertise (or allow) headers_{install,check} where inappropriate
    - Remove UML header export
    - Remove ARM26 header export
    - Fix H8300 exported headers
    - Fix m68knommu exported headers
    - Fix exported headers for SPARC, SPARC64
    - Fix 'make headers_check' on m32r
    - Fix 'make headers_check' on sh64
    - Fix 'make headers_check' on sh
    - Fix ARM 'make headers_check'
    - One line per header in Kbuild files to reduce conflicts
    - sky2 network driver device ids
    - sky2: tx pause bug fix
    - netdrvr: lp486e: fix typo
    - mv643xx_eth: fix obvious typo, which caused build breakage
    - zone_reclaim: dynamic slab reclaim
    - Fix longstanding load balancing bug in the scheduler
    - jbd: fix commit of ordered data buffers
    - ALSA: Fix initiailization of user-space controls
    - USB: Allow compile in g_ether, fix typo
    - IB/mthca: Fix lid used for sending traps
    - S390: user readable uninitialised kernel memory (CVE-2006-5174)
    - zd1211rw: ZD1211B ASIC/FWT, not jointly decoder
    - V4L: pvrusb2: Limit hor res for 24xxx devices
    - V4L: pvrusb2: Suppress compiler warning
    - V4L: pvrusb2: improve 24XXX config option descriptio
    - V4L: pvrusb2: Solve mutex deadlock
    - DVB: cx24123: fix PLL divisor setup
    - V4L: Fix msp343xG handling regression
    - UML: Fix UML build failure
    - uml: use DEFCONFIG_LIST to avoid reading host's config
    - uml: allow using again x86/x86_64 crypto code
    - NET_SCHED: Fix fallout from dev->qdisc RCU change
- enable and update patch DM02: dm-raid45 support to 2.6.18.1-20061023
- rediff patch CK01

* Wed Oct 18 2006 Thomas Backlund <tmb@mandriva.org> 2.6.18-1mdv2007.0
- update to kernel.org 2.6.18
    - see http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.18
- update patch CK01: to 2.6.18-ck1
- drop patch CK02: ck1 fix, merged upstream
- rediff patch CR01: badram support
- drop patches DA01,DA02: acpi patches, merged upstream
- drop patch DA03: asus_acpi update, merged upstream
- rediff patch DA04: acpi double proc fix
- drop patch DI03: nforce ide/sata update, merged upstream
- drop patch DI10: ata_piix probe fix, merged upstream
- rediff patch DM01: broken dmstripe fix
- disable patch DM02: dm-raid45 until upstream supports 2.6.18
- rediff patch DN02: add 47xx to b44
- drop patch DN03:  ipt_register_table correct return, merged upstream
- drop patch DN05: e1000 update, merged upstream
- rediff patch DN06: e100 update
- drop patch DN07: forcedeth, merged upstream
- drop patch DN08: sundance update, merged upstream
- update patch DN10: ipw2200 to v. 1.2.0
- drop patch DN11: ipw2200 1.1.3 wpa fix, merged upstream
- drop patch DN35: sip conntrack support, merged upstream
- drop patches DN50-DN55: old r8169 update
- drop patch DP01: via pci_quirk, should be fixed upstream
- drop patch DS01,DS04: update to alsa-1.0.12, merged upstream
- drop patch DU02: ftdi_sio testo support, merged upstream
- update patch DV01: fbsplash for 2.6.18
- drop patch DV10: v4l dvb update, merged upstream
- drop patch DV13: quickcam compilation fix, merged upstream
- update defconfigs
- use autoconf hacks from kernel-linus for now

* Sun Oct 15 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.14-1mdv2007.0
- update to kernel.org 2.6.17.14
    - Input: logips2pp - fix button mapping for MX300
    - ahci: do not fail softreset if PHY reports no device
    - MMC: Always use a sector size of 512 bytes
    - Add PIIX4 APCI quirk for the 440MX chipset too
    - xirc2ps_cs: Cannot reset card in atomic context
    - PKT_SCHED: cls_basic: Use unsigned int when generating handle
    - Fix sparc64 ramdisk handling
    - Fix serious bug in sched_clock() on sparc64
    - DVB: cx24123: fix PLL divisor setup
    - V4L: Fix msp343xG handling regression
    - sysfs: remove duplicated dput in sysfs_update_file
    - ext3 sequential read regression fix
    - Backport: Old IDE, fix SATA detection for cabling
    - NFS: More page cache revalidation fixups
    - LOCKD: Fix a deadlock in nlm_traverse_files()
    - SUNRPC: avoid choosing an IPMI port for RPC traffic
    - NFS: Fix a potential deadlock in nfs_release_page
    - dvb-core: Proper handling ULE SNDU length of 0 (CVE-2006-4623)
- add support for sparc builds
    - sync config from kernel-2.6-linus
    - build desktop(-smp) and server(-smp)
    - kernel is sparc64 (pkarlsen)
- update patch DV10: v4l dvb to 2.6.18.1 level
- drop patch DV13: merged in DV10

* Thu Sep 14 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.13-4mdv2007.0
- and hopefully the last rebuild needed after the mirror cleaning...
- stop gpg signing the rpms built on cluster, incase that is what
  is confusing the uploads...
- gpg sign the patches tarball

* Wed Sep 13 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.13-3mdv2007.0
- youri.devel screwed up the mirrors even more as it didn't build x86_64
  contrary to what was said, so as a last resort, try youri.queue from
  seggie as a last resort...
  
* Wed Sep 13 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.13-2mdv2007.0
- a simple rebuild to see if youri.devel can get the tmb kernels
  on the mirrors...

* Sun Sep 10 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.13-1mdv2007.0
- update Source4: README.kernel-tmb-sources
- updates from *mm* kernel:
    - update patch DA04: new revision of acpi double proc entry
- update to kernel.org 2.6.17.13
    - lib: add idr_replace
    - pci_ids.h: add some VIA IDE identifiers
- update to kernel.org 2.6.17.12
    - sky2: version 1.6.1
    - sky2: fix fiber support
    - sky2: MSI test timing
    - sky2: use dev_alloc_skb for receive buffers
    - sky2: clear status IRQ after empty
    - sky2: accept flow control
    - dm: Fix deadlock under high i/o load in raid1 setup
    - dm: mirror sector offset fix
    - dm: fix block device initialisation
    - dm: add module ref counting
    - dm: fix mapped device ref counting
    - dm: add DMF_FREEING
    - dm: change minor_lock to spinlock
    - dm: move idr_pre_get
    - dm: fix idr minor allocation
    - dm snapshot: unify chunk_size
    - Remove redundant up() in stop_machine()
    - Missing PCI id update for VIA IDE
    - PKTGEN: Fix oops when used with balance-tlb bonding
    - PKTGEN: Make sure skb->{nh,h} are initialized in fill_packet_ipv6() too
    - Silent data corruption caused by XPC
    - uhci-hcd: fix list access bug
    - binfmt_elf: fix checks for bad address
    - bug in futex unqueue_me
    - fcntl(F_SETSIG) fix
    - IPV6: Fix kernel OOPs when setting sticky socket options
    - SCTP: Fix sctp_primitive_ABORT() call in sctp_close()
    - SPARC64: Fix X server hangs due to large pages
    - TG3: Disable TSO by default on some chips due to hardware errata
    - Have ext2 reject file handles with bad inode numbers early
    - Allow per-route window scale limiting
    - bridge-netfilter: don't overwrite memory outside of sk
    - fix compilation error on IA64
    - INET: Use pskb_trim_unique when trimming paged unique skbs
    - spectrum_cs: Fix firmware uploading errors
    - TEXTSEARCH: Fix Boyer Moore initialization bug
- drpo patch DN60: merged upstream

* Wed Sep  6 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.11-3mdv2007.0
- mostly a rebuild to try and get the kernels on the mirrors...
- dont build laptop kernels by default
- update patch DN33: netfilter_IFWLOG from *main*

* Fri Sep  1 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.11-2mdv2007.0
- update patch DA04: updated acpi-double-proc-entries (from *mm*)
- update patch DN04: updated b44/b47 fix (from *main* kernel)
- update patch MB20: squashfs to 3.1-r2
- add patch AI01: Toshiba Equium A60 needs pci-assign-busses (MDV #18989)
- re-enable X86_GENERIC optimizations again as the mdv cluster is fixed

* Thu Aug 24 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.11-1mdv2007.0
- update to kernel.org 2.6.17.11:
    * 1394: fix for recently added firewire patch that breaks things on ppc
    * MD: Fix a potential NULL dereference in md/raid1
    * swsusp: Fix swap_type_of
    * dm: BUG/OOPS fix
    * [IPV4]: severe locking bug in fib_semantics.c 
    * IA64: local DoS with corrupted ELFs
    * ip_tables: fix table locking in ipt_do_table
    * PCI: fix ICH6 quirks
    * SERIAL: icom: select FW_LOADER
    * sys_getppid oopses on debug kernel
    * [NETFILTER]: ulog: fix panic on SMP kernels
    * tpm: interrupt clear fix
    * ipx: header length validation needed
    * disable debugging version of write_lock()
    * Fix BeFS slab corruption
    * [RTNETLINK]: Fix IFLA_ADDRESS handling
    * [NET]: add_timer -> mod_timer() in dst_run_gc()
    * [IPV4]: Limit rt cache size properly
    * sky2: phy power problem on 88e805x
    * Have ext3 reject file handles with bad inode numbers early
- update to kernel.org 2.6.17.10:
    * elv_unregister: fix possible crash on module unload
    * Fix possible UDF deadlock and memory corruption (CVE-2006-4145)
    * Fix sctp privilege elevation (CVE-2006-3745)
- drop patch DP02: merged upstream
- add code to binary rpms post scripts so we dont have to depend on
  libdrakx getting the source and build symlinks correct when binarys
  gets installed after source (MDV #24578)
- add patch AX01: fix x86_64 linking on 32bit cross-compiling
- add patch DA04: fix badness in acpi video proc_remove_entry (Danny, #22249)
- add patch DP03: add ICH7/8 ACPI/GPIO io resource quirks
- add patch DS04: update alsa to 1.0.12 final (from *mm*)

* Sat Aug 19 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.9-1mdv2007.0
- update to kernel.org 2.6.17.9
    * powerpc: Clear HID0 attention enable on PPC970 at boot time
      (CVE-2006-4093)
- re-enable patch DN55: sync r8169 with upstream 20060626, and revert
  one change that broke r8169 (Danny).
- fix patch DA01: acpi video oops on unload due to erraneous 
  semicolon (Danny)
- add patch DN60: Use pskb_trim_unique when trimming paged unique skbs
    - fixes BUG+OOPS in skbuff (from LKML)
- add patch DP01: Via pci-quirk irq behaviour change
    - reverts to a sceme that is similar to the one in 2.6.16, but 
      more restrictive (from LKML)
- add patch DP02: revert wrong pci quirks for ICH6
- add patch DM02: add support for device-mapper raid4/5 targets
- disable patch DU01: revert back to probing for new usb scheme first,
  and add a note to readme.urpmi regarding this...
- update defconfigs

* Sat Aug 12 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.8-3mdv2007.0
- really make the ps2mouse modular again :/
- add post install script magic from *mm* to cope with modular ps2mouse
  and pcspkr
- another sync from main kernel:
    - add patches DV25, DV26: Intel 965 AGP, DRM Support
    - Add patches FS11, FS12: Supermount 2.0.4 Support
- update patch MB10: ndiswrapper 1.23
    * Bug fixes to recent changes in 64-bit driver support.
    * ZyDas ZD1211 driver uses interrupt-out URBs, so set them up properly.
    * Bug fixes to Atheros USB driver support.
    * Added support for Broadcom 802.11n (draft) driver
    * Added support for 64-bit Marvell driver
    * Optimizations for 64-bit drivers
    * If network interface name changes (through udev, ifrename etc),
      ndiswrapper notices it and changes entry in procfs
- update defconfigs
      
* Fri Aug 11 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.8-2mdv2007.0
- spec cleanup
- update defconfigs
- change ps2mouse support back to modular again, since it othewise needs
  more modules to be builtin too :/
- selected updates from main kernel:
    - update patch DS01: alsa 1.0.12.rc2a
- enable CONFIG_SND_VERBOSE_PROCFS (#24231)

* Mon Aug  7 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.8-1mdv2007.0
- update to kernel.org 2.6.17.8
    - UHCI: Fix handling of short last packet
    - Fix budget-av compile failure
    - invalidate_bdev() speedup
    - cond_resched() fix
    - e1000: add forgotten PCI ID for supported device
    - ext3 -nobh option causes oops
    - PCI: fix issues with extended conf space when MMCONFIG disabled because of e820
    - Sparc64 quad-float emulation fix
    - Update frag_list in pskb_trim
    - scx200_acb: Fix the block transactions
    - Don't allow chmod() on the /proc/<pid>/ files
    - i2c: Fix 'ignore' module parameter handling in i2c-core
    - S390: fix futex_atomic_cmpxchg_inatomic
    - Fix race related problem when adding items to and svcrpc auth cache
    - ext3: avoid triggering ext3_error on bad NFS file handle
    - H.323 helper: fix possible NULL-ptr dereference
    - tty serialize flush_to_ldisc
    - ieee1394: sbp2: enable auto spin-up for Maxtor disks
    - VLAN state handling fix
    - sky2: NAPI bug
    - Add stable branch to maintainers file
    - ALSA: Don't reject O_RDWR at opening PCM OSS
    - scx200_acb: Fix the state machine
- add selected patches from upcoming main kernel:
    - DN34_ipset_svn20060804.patch
    - DN35_conntrack_sip_svn20060804.patch
    - DN40_netfilter_psd.patch
- rediff patch DN05
- update DV10: v4l/media/dvb to 2.6.18-rc3-git7 level
- drop patch DV12: merged in DV10
- make ps2mouse support builtin again
- update defconfigs
- update README.urpmi

* Wed Aug  2 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.7-3mdv2007.0
- rename patch DN11... to DN15...
- drop patch DN04, as it broke via-rhine for some (#24073)
- disable patch DN55 for now, as it broke r8169 for some...
- add patch DC01: add another via id to drm_pciids (#24021)
- add patch DF01: add generic_acl support (#24045)
- add patch DF02: add acl support to tmpfs (#24045)
- add patch DN11: ipw2200 wpa fix (#24051)
- add patch DS03: add Asus W6A support to snd-hda-intel (#19962)
- add patch DV13: fix so quickcam_messenger actually gets built (LKML)
- update defconfigs

* Fri Jul 28 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.7-2mdv2007.0
- fix kernel-tmb-source-stripped README
- fix some errors and typos in the Changelog
- fix versioning when building RC and kernels without stable patches
- selected patches from *mm*: (replacing my old patches:DN40-44 that I 
  actually forgot to apply :/ )
    - DN50_r8169-mac-address-change-support.patch
    - DN51_r8169-RX-fifo-overflow-recovery.patch
    - DN52_r8169-hardware-flow-control.patch
    - DN53_r8169-remove-rtl8169_init_board.patch
    - DN54_r8169-sync-with-vendor-s-driver.patch
- add patch DN55: sync r8169 code with 2.6.18-rc2 and upstream code
- add patch DN07: update forcedeth to 0.56
    - adds flow control (stop frame)
    - adds more ethtool support
    - adds support for MCP61 and MCP65
- add patch DN08: update sundance to 1.1
- add patch DI03: support for nVidia MCP61 and MCP65
- add patch DN11: nozomi 2.1-0.060703 for Option 3G/HSDPA support
- add patch DV12: revert VBI_OFFSET change in bttv-vbi that proke PAL
- add patches MB50-MB52: qc-usb-0.6.4 support (from *mm*)

* Tue Jul 25 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.7-1mdv2007.0
- update to kernel.org 2.6.17.7 final
- drop patches AB01-AB45: merged upstream, or fixed differently
- disable patch FS06: (update symlinks to 10) for now as it may bring 
  stack issues, need to be checked (Thierry)

* Mon Jul 24 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.6-2mdv2007.0
- drop patch FS11: (fixes bad nfs file handle triggering ext3_error)
  - it creates more problem than it fixes :-(
- sync from main kernel:
  - add patch DN05: update e1000 to v.7.1.9
  - add patch DN06: update e100 to v.3.5.14
  - add patch FS06: update supported symlinks to 10 and consecutive symlinks
    to 80 

* Sun Jul 23 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.6-1mdv2007.0
- disable X86_GENERIC optimization as the Mandriva build cluster is currently
  broken regarding -mtune=generic
- as 2.6.17.7 seems to have been delayed:
  add patches AB01-AB45: updates to 2.6.17.7-stable-preview
  * [patch 01/45] XFS: corruption fix
  * [patch 02/45] IB/mthca: restore missing PCI registers after reset
  * [patch 03/45] x86_64: Fix modular pc speaker
  * [patch 04/45] BLOCK: Fix bounce limit address check
  * [patch 05/45] memory hotplug: solve config broken: undefined reference to `online_page
  * [patch 06/45] v4l/dvb: Fix budget-av frontend detection
  * [patch 07/45] v4l/dvb: Fix CI on old KNC1 DVBC cards
  * [patch 08/45] v4l/dvb: Fix CI interface on PRO KNC1 cards
  * [patch 09/45] pnp: suppress request_irq() warning
  * [patch 10/45] Reduce ACPI verbosity on null handle condition
  * [patch 11/45] via-velocity: the link is not correctly detected when the device starts
  * [patch 12/45] 2 oopses in ethtool
  * [patch 13/45] v4l/dvb: Kconfig: fix description and dependencies for saa7115 module
  * [patch 14/45] PKT_SCHED: Fix illegal memory dereferences when dumping actions
  * [patch 15/45] PKT_SCHED: Return ENOENT if action module is unavailable
  * [patch 16/45] PKT_SCHED: Fix error handling while dumping actions
  * [patch 17/45] v4l/dvb: Backport fix to artec USB DVB devices
  * [patch 18/45] v4l/dvb: Backport the DISEQC regression fix to 2.6.17.x
  * [patch 19/45] v4l/dvb: Backport the budget driver DISEQC instability fix
  * [patch 20/45] v4l/dvb: stradis: dont export MODULE_DEVICE_TABLE
  * [patch 21/45] dvb-bt8xx: fix frontend detection for DViCO FusionHDTV DVB-T Lite rev 1.2
  * [patch 22/45] Make powernow-k7 work on SMP kernels
  * [patch 23/45] Fix powernow-k8 SMP kernel on UP hardware bug
  * [patch 24/45] cdrom: fix bad cgc.buflen assignment
  * [patch 25/45] splice: fix problems with sys_tee()
  * [patch 26/45] USB serial ftdi_sio: Prevent userspace DoS (CVE-2006-2936)
  * [patch 27/45] tpm: interrupt clear fix
  * [patch 28/45] pdflush: handle resume wakeups
  * [patch 29/45] ieee80211: TKIP requires CRC32
  * [patch 30/45] Fix IPv4/DECnet routing rule dumping
  * [patch 31/45] Add missing UFO initialisations
  * [patch 32/45] ALSA: Suppress irq handler mismatch messages in ALSA ISA drivers
  * [patch 33/45] ALSA: RME HDSP - fixed proc interface (missing {})
  * [patch 34/45] ALSA: hda-intel - Fix race in remove
  * [patch 35/45] ALSA: Fix workaround for AD1988A rev2 codec
  * [patch 36/45] ALSA: Fix undefined (missing) references in ISA MIRO sound driver
  * [patch 37/45] ALSA: fix the SND_FM801_TEA575X dependencies
  * [patch 38/45] ALSA: Fix mute switch on VAIO laptops with STAC7661
  * [patch 39/45] ALSA: Fix model for HP dc7600
  * [patch 40/45] ALSA: Fix missing array terminators in AD1988 codec support
  * [patch 41/45] ALSA: Fix a deadlock in snd-rtctimer
  * [patch 42/45] ALSA: au88x0 - Fix 64bit address of MPU401 MMIO port
  * [patch 43/45] struct file leakage
  * [patch 44/45] serial 8250: sysrq deadlock fix
  * [patch 45/45] fix fdset leakage
- update to kernel.org 2.6.17.6
  * Relax /proc fix a bit
- drop patch AA01: merged upstream
- add patch CK02: fixes idleprio and suspend to disk bug
- rediff patch: DA01
- add patch DA03: update asus_acpi to 0.30
- add patch DN04: update via-rhine to 1.4.0
- add patch DN10: update ipw2200 to 1.1.3
- add patch DN40: rtl8169: adds support for changing mac address
- add patch DN41: rtl8169: adds RX fifo overflow recovery
- add patch DN42: rtl8169: use mii registers to check/set/use hardware flow control
- add patch DN43: rtl8169: replaces rtl8169_init_board with rtl_init_phy
- add patch DN44: rtl8169: adds support for pci-e 81xx hardware (#23705)
- rediff patch: DS01
- add patch DU02: add support for testo hardware to ftdi_sio (#23666)
- add patch DV10: update linuxtv support to 2.6.18-rc2-git1 level
  * bugfixes, optimizations
  * support additional hardware with current drivers:
    - pcHDTV HD5500 HDTV
    - Kworld MCE 200 Deluxe
    - PixelView PlayTV P7000
    - NPG Tech Real TV FM Top 10
    - WinFast DTV2000 H
    - Geniatech DVB-S
    - LifeView FlyVIDEO3000 (NTSC)
    - Samsung TCPG 6121P30A
    - ...
  * support new hardware:
    - AverMedia 6 Eyes support
    - Blackbird MPEG encoder support
    - Texas Instruments TLV320AIC23B audio codec
    - Hauppauge WinTV-PVR USB2 support
    - USB Logitech Quickcam Messenger
    - GENPIX 8PSK->USB module support
    - ...
- add patch DV11: remove unused VIDIOC_S_CTRL_OLD check from matroxfb_base ioctl
- add patch FS11: fixes bad nfs file handle triggering ext3_error
- update patch MB10: ndiswrapper to 1.21
  * Calls to Miniport functions with serialized drivers (such as RT2500) 
    are serialized, so they should work with SMP.
  * Enable interrupts in IRQ handler; otherwise, some drivers (e.g., 
    Marvell 8335) don't work.
  * Kernel crash with changing mac address (with 'ifconfig hw ether ...') 
    fixed.
  * Fixes to 64-bit drivers; TI 1450 (used in AVM Fritz) is supported 
    with 64-bit.
  * Fix to SMP kernel crash when USB device is unplugged.
  * Fix to a bug (in 1.20) that locked up when used with RT2500 with SMP.
  * RT2500 is supported with 64-bit.

* Sat Jul 15 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.5-1mdv2007.0
- update to kernel.org 2.6.17.5
  * Fix nasty /proc vulnerability (CVE-2006-3626)
- Add Patch AA01: Relax /proc fix a bit as it broke hal for some 
  users (Linus Torvalds)  
  
* Thu Jul 13 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.4-1mdv2007.0
- update to kernel.org 2.6.17.4
  * fix prctl privilege escalation and suid_dumpable (CVE-2006-2451)
- add patch DA02: fix DA02_fix_AE_AML_MUTEX_NOT_ACQUIRED (#23534)
- add patch DI10: fixes ata_piix PCS-related issues and ICH8 support
- enable VIDEO_V4L1 support again even if it's marked DEPRECEATED
- update defconfigs
- reenable patch DS02: fix snd-hda-intel error handling

* Tue Jul  4 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.3-1mdv2007.0
- update to kernel.org 2.6.17.3
  * NETFILTER: SCTP conntrack: fix crash triggered by packet without 
    chunks [CVE-2006-2934]
- update to kernel.org 2.6.17.2
  * Input: return correct size when reading modalias attribute
  * idr: fix race in idr code
  * Link error when futexes are disabled on 64bit architectures
  * kbuild: bugfix with initramfs
  * ide-io: increase timeout value to allow for slave wakeup
  * libata: minor patch for ATA_DFLAG_PIO
  * ohci1394: Fix broken suspend/resume in ohci1394
  * IPV6 ADDRCONF: Fix default source address selection without 
    CONFIG_IPV6_PRIVACY
  * IPV6: Fix source address selection
  * UML: fix uptime
  * bcm43xx: init fix for possible Machine Check
  * x86: compile fix for asm-i386/alternatives.h
  * NTFS: Critical bug fix (affects MIPS and possibly others)
  * SPARC32: Fix iommu_flush_iotlb end address
  * ETHTOOL: Fix UFO typo
  * SCTP: Fix persistent slowdown in sctp when a gap ack consumes rx buffer
  * SCTP: Send only 1 window update SACK per message
  * SCTP: Reset rtt_in_progress for the chunk when processing its sack
  * SCTP: Reject sctp packets with broadcast addresses
  * SCTP: Limit association max_retrans setting in setsockopt
  * PFKEYV2: Fix inconsistent typing in struct sadb_x_kmprivate
  * IPV6: Sum real space for RTAs
  * USB: Whiteheat: fix firmware spurious errors
- fix kernel-tmb-doc building
- drop patch DN20: merged upstream
- update patch FS01: unionfs to v. 1.3
- drop patch FS02: merged upstream
- make kernel-source(-stripped) provide: kernel-source-fbsplash so 
  it works with fbsplash-utils (Danny)

* Sat Jun 24 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17.1-1mdv2007.0
- update to kernel.org 2.6.17.1
  * CVE-2006-3085
- redo patch CE02: acpi-dsdt-initrd to match updated ACPI in DA01
- drop patch CE11: acpi-ec-nospinlock, as its merged in DA01
- add patch DA01: update ACPI support to 20060608 
- add patch DS01: update ALSA to 1.0.12rc1
- disable patch DS02: snd-hda-intel error-handling as it should be fixed
  in the updated alsa
- update patch MB10: ndiswrapper to 1.18
  * Support for RNDIS was broken in 1.16; they work now
  * Suspend/resume improved
  * Netpoll support added
  * Support for RNDIS driver with Vista drivers for 64-bit
  * Fix Kernel crash with RT2500 under heavy load
- drop Obsoletes on virtual rpms

* Tue Jun 20 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17-2mdv2007.0
- Fix EXTRAVERSION when no stable patch applied ( now where did I put
  my brown paper bag ??? )

* Sun Jun 18 2006 Thomas Backlund <tmb@mandriva.org> 2.6.17-1mdv2007.0
- update to kernel.org 2.6.17
- update CK01 to 2.6.17-ck1
- drop patches merged upstream: CA73, CP03, CP10, DC01, DC11, DN10, 
  DN37, DN38, DN39, DS01, DV02, FS20
- rediff patches: CR01, DI08, DM01, DN02
- add patch DN20: fix bcm43xx init-vs-irq workaround
- disable BLK_DEV_UB as it conflicts with usb-storage (#23159)
- add info to README.urpmi regerding modular PS2 (#23141)

* Sat Jun 17 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.20-4mdv2007.0
- add patch CP10: fix nVidia HPET timer override
- add patch DC01: add drm from 2.6.17-rc6-git7 to match xorg 7.1
- add patch DC11: fixes pptp large data transfer random hangs
- add patch DN10: update to forcedeth 0.54
- add patch FS20: add autofs5 support from 2.6.17-rc6-git7 (#22399)

* Sun Jun 11 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.20-3mdv2007.0
- rework rhconfig.h for autoconf, and fix a typo
- enable in defconfig as module: BT_CMTP (Michael Braun)
- enable in defconfig: KEXEC (Raphael Gertz)
- disable in defconfig FB_TILEBLITTING as it conflicts fbsplash 
- add patch CP03: update powernow-k8 to 1.60.1
- add patch DU01: enable usbcore old_scheme_first to fix error:
  "device not accepting address"
- add patch CR01: add support for BadRAM (poor mans "IBM ChipKill")(from *mm*)
- add patch DV01: fbsplash 0.9.2-r5 (from *mm*)
- add patch DV02: fix fbsplash build (from *mm*)

* Sat Jun 10 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.20-2mdv2007.0
- Update patch CK01 to 2.6.16-ck12
- Update patch FS01 to unionfs-1.2
- Drop old patch FS02 as it didnt fix the unionfs smp bug
- Add new patch FS02 to fix unionfs Makefile versioning
- Spec fixes: dont strip scripts dir in source-stripped rpm, and some typos
- Update README.urpmi with info regarding need to recreate initrd and rerun
  lilo for first time istallers...
- enable HIGHPTE for HIGHMEM4G & HIGHMEM64G in create_configs
- enable following defconfig options:
  * EMBEDDED, PACKET_MMAP, NET_SCH_CLK_CPU, PNPBIOS_PROC_FS, TULIP_NAPI,
    TULIP_NAPI_HW_MITIGATION, AMD8111E_NAPI, ADAPTEC_STARFIRE_NAPI, 
    8139TOO_8129, VIA_RHINE_MMIO, E1000_NAPI, R8169_NAPI, IXGB_NAPI, 
    S2IO_NAPI, IPW2100_MONITOR, PC300_MLPPP, SERIAL_8250_SHARE_IRQ, 
    IPMI_PANIC_EVENT, IPMI_PANIC_STRING, WATCHDOG_NOWAYOUT, WDT_501_PCI, 
    FT_PROC_FS, USB_DYNAMIC_MINORS, USB_SUSPEND, USB_SERIAL_SAFE_PADDED
- disable following defconfig options:
  * NET_SCH_CLK_GETTIMEOFDAY, MOUSE_ATIXL, TOUCHSCREEN_ADS7846, RISCOM8, 
    LEGACY_PTYS, DVB_USB_DIBUSB_MB_FAULTY, FB_HGA_ACCEL, FB_ATY_GENERIC_LCD, 
    FB_3DFX_ACCEL, FB_TRIDENT_ACCEL, FB_GEODE, MDA_CONSOLE, 
    FRAMEBUFFER_CONSOLE_ROTATION, FONT_10x18, USB_LIBUSUAL, 
    USB_HIDINPUT_POWERBOOK, USB_APPLETOUCH

* Mon Jun  5 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.20-1mdv2007.0
- fix another error in rhconfig.h (Doh :/ )
- update to kernel.org 2.6.16.20
- drop patch DI03 (merged upstream)
- rediff patch DN39
- re-enable LVM & cfor laptop kernels

* Sat Jun  3 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.19-4mdv2007.0
- fix rhconfig.h autoconf breakage 
- update patch MB30: acerhk to version 0.5.33
- add patch MB40: acer_acpi - the acerhk clone for x86_64
- enable USB_EHCI_ROOT_HUB_TT

* Sat Jun  3 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.19-3mdv2007.0
- a simple rebuild on n2 to see if n5 produces broken kernel rpms

* Thu Jun  1 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.19-2mdv2007.0
- enable X86_BIGSMP for ix86 smp kernels to support cpu hotplugging
- enable USB_EHCI_SPLIT_ISO for all kernels
- add patch CP02: disable only 12.5 duty cycle in p4-clockmod on errata N60,
  not everything below 2 GHz
- add patch DI03: help resume from libata
- add patch DN03: fix ipt_register_table() wrongly return 0 instead of
  error code when xt_register_table() fails
- fix automatic upgrades because of name change:
  * make desktop(-smp)-latest obsolete desktop686(-smp)-latest <=2.6.16.18-3
  * make desktop586(-smp)-latest obsolete desktop(-smp)-latest <=2.6.16.18-3

* Wed May 31 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.19-1mdv2007.0
- update to 2.6.18.19
  * Netfilter: CVE-2006-1343
- more spec cleanups...
- fix defconfig-maximum on ix86
- add more patches from *mm* series:
  - add patch DB32: SiS 965 IDE support
  - add patch DI02: prevent disk spindown on reboot
- add patch CP01: HOTPLUG_CPU must depend on !X86_PC (#22594)
- add patch DS02: fix Alsa intel hda error handling (Danny)

* Tue May 30 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.18-4mdv2007.0
- do some renaming of the desktop flavours to be consistent with mm series
  * old i586,1GB desktop(-smp) is now desktop586(-smp)
  * old i686,4GB desktop686(-smp) is now desktop(-smp)
- require bootloader-utils >= 1.12-1mdv2007.0 wich is fixed for the
  above name change...
- update support files for new names, so autoconf still works.
- sync laptop configs with the mm series
- create_configs cleanup and fixing for new naming
- update defconfigs, some syncs from multimedia series:
  * disable following config options:
    AUDIT, AUDITSYSCALL, DETECT_SOFTLOCKUP, FORCED_INLINING
  * enable following config options:
    MODVERSIONS, MODULE_SRC_VERSION_ALL, X86_MCE_NONFATAL, X86_REBOOTFIXUPS,
    APM_ALLOW_INTS, APM_REAL_MODE_POWER_OFF, CPU_FREQ_DEFAULT_GOV_USERSPACE, 
    CPU_FREQ_GOV_USERSPACE, NET_SCH_CLK_GETTIMEOFDAY, SERIAL_8250_CONSOLE,
    SERIAL_8250_ACPI, SERIAL_8250_EXTENDED, SERIAL_CORE_CONSOLE, CRAMFS,
    NFS_DIRECTIO
  * enable/change following config options as/to modules:
    CPU_FREQ_GOV_PERFORMANCE, BINFMT_MISC, PACKET, INET_DIAG, INET_TCP_DIAG,
    IEEE1394, MII, INPUT_MOUSEDEV, AGP, USB_KBD, USB_MOUSE

* Sat May 27 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.18-3mdv2007.0
- use 'distsuffix' macro for rpmtag so it's correct on both 2006.0 and 
  Cooker / 2007.0
- add *tmb* to 'uname -r' to differentiate against upcoming *mm*, 
  as we now use same naming scheme...
- add support for flavours laptop and laptop-smp, and their virtual rpms, 
  but dont build them by default
- selected patches from main kernel:
  - add patch CA03: boot in 80x25 videomode if users selects unsupported mode
  - add patch DB25: fix megaraid_mbox sysfs name
  - add patch DI08: enable ATAPI support in libata
- selected pateches from multimedia kernel:
  - add patch CA73: fixes crash in powernow-k8

* Thu May 25 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.18-2mdv2007.0
- fix README.urpmi text
- fix x86_64 server-smp summary
- change rpmtag s/mdk/mdv/ (also used in 'uname -r')
- kernel-tmb now goes 'mkrel' for rpm names, but not for 'uname -r'
- update requires on bootloader-utils to 1.10-mkrel 2
- update requires on mkinitrd to 4.2.17-mkrel 20
- switch from Requires to Requires(pre) for compiled kernels
  to make sure all support files are in place at install time
- disable generation of useless debug rpms

* Tue May 23 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.18-1mdk
- update to kernel.org 2.6.16.18
- hang on to you hats ;-), CONFIG_PARTITION_ADVANCED is enabled 
  again, allong with: CONFIG_OSF_PARTITION, CONFIG_MAC_PARTITION,
  CONFIG_LDM_PARTITION, CONFIG_KARMA_PARTITION
  please report any problems you may have...

* Sun May 21 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.17-1mdk
- update to kernel.org 2.6.16.17
- update CK01 to 2.6.16-ck11
- drop ZZ01 as it's included in 2.6.16.17
- for server sets, set HZ_100, enable CPUSET
- add README.urpmi regarding modular ide
- change CONFIG_SND to module
- selected patches from main kernel
  - add patch DN01: add module alias to bonding
  - add patch DN02: adds bcm47xx support to b44
  - adds patches DN37,DN38,DN39: support for wireless softmac, 
    prism54usb, bcm43xx, adm8211, tiacx
  - add patch DS01: Alsa 1.0.11
  - add patch FQ01: cpufreq speedstep support for dothan
  - add patch FS10: fixes oops in destroy_inode
  - add patches MB01,MB02: 3rdparty framework
  - add patch MB10: ndiswrapper 1.16
  - add patch MB20: squashfs 3.0
  - add patch MB30: acerhk 0.5.18

* Sat May 20 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.16-6mdk
- fix mkinitrd requires s/-/>=/ 
- change requires on mkintrd and bootloader-utils to match 'mkrel'
  for packages rebuilt for 2006.0
- fix typo in kernel-tmb.patchlist

* Fri May 18 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.16-5mdk
- first build with new toolchain (gcc-4.1.1, glibc 2.4.0)
- add patch ZZ01: CVE-2006-0039 Netfilter race, oops, info leak
  * (from upcoming -stable 2.6.16.17)
- fix create_configs for server-smp to serversmp change
- update FS01: to unionfs snapshot 20060503-0408
- add FS02: unionfs smp oops fix (Junjiro Okajima (unionfs developer))
- update requires on bootloader-utils to 1.10-1mdk
  * adds support for kernel-tmb sets in kheader, needed for autoconf
- update requires on mkinitrd to 4.2.17-19mdk
  * makes ide-controller statement in modprobe.conf optional when
    installing a kernel with ide support built-in
  
* Tue  May 16 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.16-4mdk
- fix PrepareKernel and create_configs breakage due to versioning change
- change CONFIG_EDD from module to builtin
- add patch DM01: adds boot parameter broken_dmstripe to allow unaligned 
  dm-stripe partitions to get activated...

* Sat May 13  2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.16-3mdk
- change kprovides and requires for source-stripped
- drop unneeded kernel-tmb-latest virtual rpm
- fix missing parts of rhconfig.h (source15) to get autoconf working again
- update CE02_acpi-dsdt-initrd to v0.8.1-2.6.16 (Eric Piel)
- change RTC from module to built-in
- change IP_NF_CONNTRACK from built-in to module
- use tarball patches.description as kernel-tmb.patchlist to not duplicate work
- add patch FS01: Unionfs snapshot 20060423-1600

* Wed May 11 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.16-2mdk
- fix pre, post, postun scripts to match change in versioning
- fix autoconf , rhconfig and version.h generation to match the 
  versioning change ...
- keep a list of patches in kernel-tmb.patchlist outside patches 
  tarball so it shows up in Mandriva CVS ...

* Wed May 11 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.16-1mdk
- update to 2.6.16.16
- update CK01 to 2.6.16-ck10
- fix CE02_acpi-dsdt-initrd to acually get it selectable (Udo Rader)
- readd needed arch/i386/kernel/sigframe.h to -stripped source (rapsys)
- strip a few more files from -stripped source
- rename /boot/(vnlinuz,initrd)-* to match naming of other kernels
  to ease installer/bootloader-utils support (Request by Pixel)

* Mon May  8 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.14-1mdk
- update to 2.6.16.14
- fix scripts build (needed for external modules)
- create a really slip-streamed kernel-tmb-source-stripped 
  (~14MB vs main ~65MB)

* Wed May  3 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.13-1mdk
- quick update to 2.6.16.13

* Tue May  2 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.12-1mdk
- update to kernel.org 2.6.16.12
- update patch CK01 to 2.6.16-ck9
- NOTE: This nice system with kernel metapackages to allow for
  automated updating of kernels and kernel-source without breaking
  current installs is pretty much what Oliver Thauvin already suggested
  in 2004-12-07 !! For more info see Bugzilla #21345 comment 26.
  So many thanks to Oliver for this!!

* Mon May  1 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.11-4mdk
- add patches.description in patches tarball to keep track of patches
- patch CE02: add support for custom DSDT in initrd
- patch CE11: acpi_ec_no_spinlock (Udo Rader)
- patch CK01: Con Kolivas patchset 2.6.16-ck8
  * smpnice, staircase scheduler, swap prefetch, readahead, ...
- patch DN33: netfilter IFWLOG support (Gertz Raphael)
- update defconfigs for the above patches
- disable swap prefetch for server(-smp) kernels
- set HZ_1000 on desktop sets, HZ_100 on server sets
- fix description for ix86 desktop kernels to mention the fact
  that only 870-900MB RAM is detected (even if marked 1GB)...
- enable SERIAL_NONSTANDARD support (Gertz Raphael)
- add provides kernel to cope with basesystem requires
- make ide fully modular (so you need: alias ide-controller 'modulename' 
  in /etc/modprobe.conf or fixed initrd to detect modular ide
- add metapackages for every kernel flavour to allow for auto-updating
  kernels/souce with urpmi --auto-select without removing the previous one:
  * kernel-tmb-desktop-latest, kernel-tmb-desktop-smp-latest
  * kernel-tmb-desktop686-latest, kernel-tmb-desktop686-smp-latest
  * kernel-tmb-server-latest, kernel-tmb-server-smp-latest
  * kernel-tmb-source-latest, kernel-tmb-latest (shows all flavours)
- fix version.h generation
- specfile cleanups & fixes

* Tue Apr 25 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.11-3mdk
- set CONFIG_PHYSICAL_START=0x400000 (Thierry)
- make md modular (Luca)

* Tue Apr 25 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.11-2mdk
- readd versioned package names
- disable CONFIG_PARTITION_ADVANCED (Raphael)

* Tue Apr 25 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.11-1mdk
- update to 2.6.16.11
- fix configs for missing initrd (doh...)
- set server(-smp) kernels to use HZ_1000 (Luiz)

* Thu Apr 20 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.9-1mdk
- update to 2.6.16.9

* Wed Apr 19 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.8-1mdk
- update to 2.6.16.8

* Tue Apr 18 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.6-1mdk
- update to 2.6.16.6

* Tue Apr 18 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.5-3mdk
- more spec cleanups
- create_config script cleaning

* Mon Apr 17 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.5-2mdk
- optimize configs
- fix descriptions

* Sun Apr 16 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16.5-1mdk
- update to 2.6.15.5
- fix spec and support files for stable extraversion release

* Sun Apr 16 2006 Thomas Backlund <tmb@mandriva.org> 2.6.16-1mdk
- Alive Again !!! ... ;-)
- Scrap the old versioning as I don't track main kernel anymore...
- Start fresh from unpatched kernel
- Switch to kernel.org versioning.
- build desktop up & smp kernels:
  * i586, 1GB. CFQ Scheduler, Voluntary Preempt
  * x86_64, CFQ Scheduler, Voluntary Preempt
- build i686 optimized desktop686 up & smp kernels:
  * i686, 4GB, CFQ Scheduler, Voluntary Preempt
- build server up & smp kernels: 
  * i686, 64GB, Deadline Scheduler, No Preempt
  * x86_64, Deadline Scheduler, No Preempt
- build as modular as possible
- use  MDV Releasespecific rpmname
- redo spec and support files to match all changes

* Tue Aug 31 2004 Svetoslav Slavtchev <svetljo@gmx.de> 2.6.7-2.tmb.6mdk
- yet another tiny resync with -mm3
	MC50_ndiswrapper-0.10.tar
	MD10_ivtv-0.1.10-pre2-ck104y.tar
	MG70_ipw2100-0.53_and_ipw2200-0.4.tar
- add ecc driver (from -mm3)
	ZS58_ecc.patch
	ZS59_ecc-fix.patch
- add drbd-0.7.1 (from -mm3)
	ZS20_drbd-0.7.1.patch
	ZS21_drbd-add_drbd_buildtag.patch
- add cluster support and gfs (from -mm3)
	ZC01_cman.patch
	ZC02_cman_integrate.patch
	ZC03_dlm.patch
	ZC04_dlm_integrate.patch
	ZC05_VFS_call_down_into_FS_on_flock_calls.patch
	ZC06_lock_harness.patch
	ZC07_lock_harness_integrate.patch
	ZC08_gfs.patch
	ZC09_gfs_integrate.patch
	ZC10_lock_nolock.patch
	ZC11_lock_nolock_integrate.patch
	ZC12_lock_dlm.patch
	ZC13_lock_dlm_integrate.patch
	ZC14_lock_gulm.patch
	ZC15_lock_guilm_integrate.patch
	ZC16_gnbd.patch
	ZC17_gnbd_integrate.patch
- fix kernel-BOOT compile
	thinkpad depends on CONFIG_PM
	GFS depends on CONFIG_IPV6

* Mon Aug 09 2004 Svetoslav Slavtchev <svetljo@gmx.de> 2.6.7-2.tmb.5mdk
- build win4lin kernels too
- disable dxr3 on alpha 
  alpha should build happily again :-)

* Mon Aug 09 2004 Svetoslav Slavtchev <svetljo@gmx.de> 2.6.7-2.tmb.4mdk
- re-add alsa addons
	DS10_alsa-1.0.5_addons.tar
	DS11_echoaudio-0.8.10.tar
	DS20_alsa_usx2y_fixes.patch
	DS21_alsa_usx2y_build.patch
	DS22_alsa_usx2y__usbaudio_exports.patch
	DS23_alsa_hdspm_include.patch
	DS24_alsa_echoaudio_integrate.patch
	DS25_alsa_pdplus_integrate.patch
	DS27_alsa_msnd_integrate.patch
	DS28_alsa_serialmidi_integrate.patch
	DS29_alsa_serialmidi_k2.6cleanups.patch
	DS30_alsa_msnd_include_pnp.h.patch
	DS31_alsa_echoaudio_export_no_symbol.patch
	DS32_alsa-atiixp_modem_integrate.patch
	DS33_alsa-emu10k1x_integrate.patch
	DS34_alsa_audigyls_integrate.patch
	DS35_alsa_audigyls_20040612.patch
	DS36_alsa_snd_amagic.h.patch
	DS37_alsa_sound_opti92x-ad1848-locking-fix.patch
	DS38_alsa_add_tvmixer.patch
- 3rdparty resync with -sds
	DV16_epcam-linux2.6.1.patch
	DV17_vpx3224.patch
	MB20_eagle-usb-1.9.8.tar
	MB30_hostap-0.2.4.tar
	MB46-lirc_serial_sir_split.patch
	MB70_dfg1394-1.3.tar
	MB80_1prism25-0.2.1-pre21.tar
	MB90_ov511-2.28.tar
	MB91_ov511_mark_in-kernel_driver_as_old.patch
	MC20_bcm5700-7.3.5.tar
	MC30_at76c503a-cvs20072004.tar
	MC50_ndiswrapper-0.9.tar
	MC70_acecad-3.1.tar
	MC71_acecad-3.1-hid.patch
	MD00_lpfcdriver-2.6-8.0.7.tar
	MD10_ivtv-0.1.10-pre2-ck101.tar
	MD70_fuse-1.3.tar
	ME10_shfs-0.35.tar
	ME20_usbvision0.9.6cvs20040717.tar
	ME30_gatos-km-cvs20040719.tar
	ME40_cdfs-2.6.3.tar
	ME60_exaudio-1.62.tar
	ME61_exaudio_lirc_path.patch
	ME70_spca5xx_26x-10072004.tar
	ME71_spca50x_mdelay.patch
	ME80_qcamvc-1.0.7cvs20040608.tar
	ME90_pvfs2-0.1.1.tar
	MF20_dyc_ar5k.tar
	MF21_dyc_ar5kmod_drop_stdio_include.patch
	MF30_ibmcrypto.tar
	MF40_fpi2002-0.1.tar
	MF41_fpi2002_k26.patch
	MF50_cxacru_2003-10-05.tar
	MF51_cxacru-2.6.x_add_ids_to_speedtch.patch
	MF60_cpad-0.2.tar
	MF61_cpad26-0.1_use_kconfig.patch
	MF62_cpad_blacklist_cpad_in_hid.patch
	MF70_acx100-0.2.0pre8_plus_fixes_23.tar
	MF80_thinkpad-5.5.tar
	MF90_subfs_submount-0.9.tar
	MG10_prism54_usb-cvs20040621.tar
	MG20_rhineget.tar
	MG21_rhine_main.patch
	MG22_rhineget_depend_on_NET_and_X86.patch
	MG30_rfswitch-0.1.tar
	MG31_rfswitch_merge_fix.patch
	MG40_fsam7400-0.3.1.tar
	MG50_zr364xx-0.52.tar
	MG60_v3tv-v4l2_cvs20040717.tar
	MG70_ipw2100-0.51.tar
	MG90_omnibook-2004-07-01.tar
	MG91_omnibook-cpufreq.patch
	MG92_omnibook_Makefile_fix_alt1.patch
	MH00_mod_marvel-cvs20031215.tar
	MH00_mod_marvel.desc
	MH10_gpib-3.2.00.tar
- security fixes
	ZG51_1100_ip_tables.patch
	ZG52_1105_CAN-2004-0497.patch
	ZG53_1110_proc.patch
	ZG54_1325_iptables-headers.patch
	ZG55_1115_net_eql.patch

* Thu Jul 15 2004 Thomas Backlund <tmb@mandrake.org> 2.6.7-2.tmb.3mdk
- fix BOOT compiling
- update squashfs to 2.0 Final (MC80)
  * Initrds are now supported for kernels 2.6.x.
  * amd64 bug fixes.
  * Check-data and gid bug fixes.

* Wed Jul 14 2004 Thomas Backlund <tmb@mandrake.org> 2.6.7-2.tmb.2mdk
- bootsplash is back (CD01, CD04) (from sds15)
- rediff (CK01) because of bootsplash
- update Win4Lin patch to 2.6.7 (P100)
- update mki-adapter26 to 1.3.6 (P101)
- drop libata vs. pata piix fix (DI11), let the user choose
  between libata and pata piix support
- drop the outdated hfsplus from 3rdparty (MD30, MD31, MD32)
- BadRAM support is back (ZS04)
- uss725 works again (DU02, DU07, DU08) (from sds15)
- Cloop 2.0.1 is back (ZS18, ZS19) (from sds15)

* Wed Jul 07 2004 Thomas Backlund <tmb@mandrake.org> 2.6.7-2.tmb.1mdk
- full restart from main 2.6.7.2mdk to get back in sync with main
  (meaning it may have less hw support and features than my 2.6.5 
   series now in the beginning until I have synced up with sds15...)
- first tmb kernel to be uploaded to amd64 contribs
- build kernels with preempt
- changelog will from now on always reference the patches with
  their prefix to make it easier to keep track of changes
- restructure patches tarball for easier maintenance:
  * all alsa specific patches now using DS prefix
  * 3rdparty driver tarballs now have patches affecting them directly 
    after the tarball. Tarballs now starts from prefix MB10 and will
    have room for 9 patches reserved, meaning next tarball will get
    MB20 and so on...
- alsa 1.0.5 (DS01) (from sds15)
- update alsa to 1.0.5a (DS02) (from sds15)
- move (old DA54) alsa hp quirk fix to (DS03)
- fix dell laptop alsa hang (DS04) (from sds15)
- move (old MC01) acx100 to (MB10) and update to 0.2.0pre7-fixes6 (from sds15)
  * move (old MD01) compil fix to (MB11)
- move (MC02) eagle-usb to (MB20) and update to 1.9.7cvs (from sds15)
  * drop claiminterface fix (old MD02)
  * move (old MD02) mdelay fix to (MB21)
- move (old MC03) hostap to (MB30) and update to 0.2.2cvs20040609 (from sds15)
  * add build integration fix (MB31) (from sds15)
- move (old MC04) lirc to (MB40)
  * move (old MD04) buildfixes to (MB41)
  * move (old MD05) devfs fixes to (MB42)
  * move (old MD06) parport enumarate fix to (MB43)
  * move (old MD07) atiusb fix to (MB44)
  * add floting point fix (MB45) (from sds15)
- move (old MC05) lufs to (MB50)
  * add support for extra opts (MB51)
- move (old MC07) qc-usb to (MB60) and update to 0.6.0
- move (old MC08) dfg1394 to (MB70) and update to 1.1cvs20040314 (from sds15)
  * drop irq interval fix (old MD08)
  * add dfg1394 firewire init fix (MB71) (from sds15)
- move (old MC09) prism25 to (MB80) and update to 0.2.1-pre20 (from sds15)
- move (old MC10) ov511 to (MB90)
- move (old MC11) dxr3 to (MC00) and update to 0.14_200403013 (from sds15)
  * drop i2c fix (old MD11)
- move (old MC12) iscsi to (MC10)
  * move (old MD12) iscsi shost fix to (MC11)
- move (old MC13) bcm57xx to (MC20) and update to 7.1.22
  * drop buildfixes (old MD13)
  * add ULL fix (MC21)
- move (old MC15) at76c503 to (MC30) and update to 0.12beta14 (from sds15)
- move (old MC16) vc_ar5k to (MC40)
- move (old MC17) ndiswrapper to (MC50) and update to 0.7 (from sds15)
- move (old MC18) mod_marvel to (MC60) and update to marvel_mgatv cvs20040408 (from sds15)
- move (old MC19) acecad to (MC70)
  * move (old MD19) cur_altsetting fix to (MC71)
- move (old MC20) squashfs to (MC80) and update to 2.0
- move (old MC21) bcm44xx to (MC90)
- drop old lpfc driver (old MC23)
- add new lpfcdriver ver 20040409 (MD00) (from sds15)
- move (old MC24) ivtv to (MD10) and update to 0.1.10-pre2-ck97h (from sds15)
  * drop i2c fix (old MD24)
  * fix includes (MD11) (from sds15)
  * use kernel min/max for msp3400 (MD12) (from sds15)
- move (old MC25) rivatv to (MD20) and update to cvs20040626 (from sds15)
  * drop old tweaks (old MD25)
  * add new tweaks (MD21) (from sds15)
- move (old MC26) hfsplus to (MD30)
  * move (old MD26) quiet build fix to (MD31)
  * move (old MD27) drop gendisk fix to (MD32)
- move (old MC27) viahss to (MD40)
- move (old MC28) w9968cf to (MD50)
  * move (old MD28) i2c fix to (MD51)
  * remove misplaced semicolon (MD52) (from sds15)
- move (old MC29) poldhu to (MD60)
  * move (old MD29) no CardServices fix to (MD61)
- move (old MC30) fuse to (MD70)
  * move (old MD30) modversions fix to (MD71)
- move (old MC32) svgalib_helper to (MD80)
  * move (old MD32) buildfixes to (MD81)
- move (old MC33) ogfs to (MD90)
- move (old MC34) iteraid to (ME00) and update to 1.45
- move (old MC35) iteraid includes fix to (ME01)
- move (old MC36) shft to (ME11)
- fix BugZilla #10057
  * re-enable CONFIG_BLK_DEV_PIIX
  * disable pata piix driver support only for controllers
    covered by the libata piix driver (DI11)
- add ipw2100-0.46_3 (DN50) (from sds15)
  * add docs, Kconfig and Makefile change (DN51) (from sds15)
  * add support for Fujitsu-Siemens Amilio 7400 (DN52) (from sds15)
    * add KConfig (DN53) (from sds15)
  * compile with HOSTAP CVS (DN54) (from sds15)
- kernel command line needs to support more args (CA07)
- fix zh_cn coding error in nls codepage 939 (FN10) (BugZilla #360)
- fix pwc driver (DV13) (from sds15)

* Wed Jun 02 2004 Thomas Backlund <tmb@mandrake.org> 2.6.5-1.tmb.6mdk
- update iteraid to 1.45 (MC41, MC42)
  * 64bit fixes, works on amd64
- fix zh_cn coding error in nls codepage 939 (FN10) (BugZilla #360)

* Fri Apr 30 2004 Thomas Backlund <tmb@mandrake.org> 2.6.5-1.tmb.5mdk
- iteraid 1.44
- fix kernel-source include strip for ppc64
- disable CONFIG_FB_ATY_XL_INIT in ppc
- add workaround for ppp_mppe from 2.4 series
- misc fixes and addons from 2.6.5-sls9 (Svetljo)
  * support for VIA CLE266 framebuffer
  * support for VIA6410 IDE and VIA6421 SATA
  * acpi 20040426, processor-load, link-tolerant
  * cpufreq 20040419, userspace warning
  * nForce2 ioapic fix
  * nForce2 idle lockups fix

* Fri Apr 16 2004 Thomas Backlund <tmb@mandrake.org> 2.6.5-1.tmb.4mdk
- fix BOOT compiling

* Thu Apr 15 2004 Thomas Backlund <tmb@mandrake.org> 2.6.5-1.tmb.3mdk
- fix posix-timers to have proper per-process scope
- update Netraverse Win4Lin patch to 2.6.5
- CAN-2004-0075-vicam (Svetljo)
- CAN-2004-0177-ext3 (Svetljo)
- CAN-2004-0109 isofs fix (Svetljo)
- fix for synaptics (Svetljo)

* Tue Apr 13 2004 Danny Tholen <obiwan@mailmij.org> 2.6.5-1.tmb.2mdk
- remove broken old hfs patches
- patch orinoco drivers to fix Tx timeouts
- patch for oops with tumbler/snapper cards
- disable preempt on smp for ppc (broken)

* Tue Apr  6 2004 Thomas Backlund <tmb@mandrake.org> 2.6.5-1.tmb.1mdk
- kernel.org 2.6.5
- alsa 1.0.4 final (Svetljo)
- alsa addons + fixes (Svetljo)
- echoaudio 0.8.10pre1 (Svetljo)
- acpi4asus 0.28 (Svetljo)
- scsi updates (Svetljo)
- Amd K8PowerNow ACPI (Svetljo)
- ipw2100 v0.39 (Svetljo)
- orinoco cvs 20040328 + monitor mode support (Svetljo)
- tv / dvb card support updates (Svetljo)
- cifs 1.0.5cvs (Svetljo)
- ReiserFS updates/fixes (Svetljo)
- packet writing, dvd-/+rw support (Svetljo)
- TI cardbus IRQ routing fixes (Svetljo)
- ipmi updates (Svetljo)

* Sun Apr 4 2004 Danny Tholen <obiwan@mailmij.org> 2.6.4-1.tmb.6mdk
- ppc fixes and rebuild:
  * preempt fixes
  * syscall and keywest fixes
  * add therm_adm103x module
  * map sysrq on ibook/powerbook keyboard to f11
  * fix config

* Wed Mar 24 2004 Thomas Backlund <tmb@mandrake.org> 2.6.4-1.tmb.5mdk
- fix iteraid module includes
- change descriptions to Mandrakelinux
- fix amd64 rpm building
- add the missing drm_ioctl32 fixes for amd64

* Wed Mar 24 2004 Thomas Backlund <tmb@mandrake.org> 2.6.4-1.tmb.4mdk
- add two new compile flags to src.rpm:
  * '--with win4lin' will compile the kernels with win4lin support,
    and the kernels will be named kernel-tmb-win4lin-...
  * '--with laptop' will compile the kernel with laptop-specific
    changes, currently the only change is to make USB support builtin,
    as it's currently needed for synaptics to work...
- merge x86_64 spec changes from main kernels
- use Dannys modules.description generation workaround until
  module-init-tools are updated...

* Tue Mar 23 2004 Thomas Backlund <tmb@mandrake.org> 2.6.4-1.tmb.3mdk
- fix specfile rm -rf for ppc(64) and missing 'asm-' in *x86* includes
  * thanks to Danny for reporting this
- remove orinoco 0.14alpha2 patch, it's to buggy at this stage...
- drop lirc patch MD07, as it's merged in the updated MD05
- fix ZS99 menu-cleanups patch to actually allow ppc builds (Danny)
- new ppc(64) configs (Danny)
- map sysrq to powerbutton on power and ibooks (Danny)
- acpi 20040311 (Svetljo)
- update packet writing support (Svetljo)
- support ITE it8212 RAID chip (Svetljo)

* Sun Mar 21 2004 Thomas Backlund <tmb@mandrake.org> 2.6.4-1.tmb.2mdk
- initial support for ppc64
- make smaller kernel-source package
  * initial patch by Svetljo ;-)
  * add even more rm -rf to the spec file based on arches groups
    - groups are: alpha, ix86/amd64, ppc/ppc64, sparc/sparc64
    - rebuilding for one group removes sources for the 3 others
- add newline to patch MD14
  * gets rid of 'patch unexpectedly ends in middle of line' message
- selected sync with main 2.6.3-7mdk
  * x86_64 really disable IO-APIC on NVIDIA boards (gb)
  * edd get legacy parameters.
  * ide-scsi error handling fixes.
  * tun name fix.
  * at76c503a 0.12 Beta8 with MSI6978 Wlan PC2PC support.
  * d_alloc_root, vma corruption, ramdisk memleak fixes.
  * loop setup race fix.
  * AMD 768MPX bootmem fix.
  * bootsplash 3.1.4
  * fix ipmi build
- drop CardServices Compability Layer (it's broken)
- fix ini9100u build
- fix kernel threading
- forcedeth 0.25
- orinoco 0.14alpha2
- pcmcia 2.6.5-rc2
- usb 2.6.5-rc2
- ndiswrapper 0.6
- ipw2100 v0.36
- always show kernel version in oops, as people tend to forget
  to report this crucial information
- drop patch DU02, it makes usb hang on shutdown

* Thu Mar 11 2004 Thomas Backlund <tmb@mandrake.org> 2.6.4-1.tmb.1mdk
- resync with kernel.org 2.6.4
  * dropped 103 patches merged upstream
- disable packet writing support :-(  until it's updated to 2.6.4

* Thu Mar 11 2004 Thomas Backlund <tmb@mandrake.org> 2.6.3-4.tmb.3mdk
- BadRAM support for ix86 (initial patch by Udo Rader)
  * fixed bug that disabled __free_page(page) if BadRAM is disabled
  * modified so it actually builds with tmb kernels
  * modified so that it's possible to build a kernel with it disabled
  * add BadRAM info to /proc/meminfo 
- clean 3rdparty mod_marvel tarball
- remove 3rdparty Makefile with mrproper, as it's autogenerated
- set CONFIG_8139_RXBUF_IDX=2, was set for embedded systems...  :-( 
- ndiswrapper 0.5
- Intel Pro Wireless 2100 (centrino) 0.29
- update sis190 and sis900 nics
- update pcnet32 to 1.28, fixes hangs
- updated alpha and sparc64 configs (Stefan)
- updated ppc config (Danny)
- aic79xx 20040209 (svetljo)
- acpi 2004020 (svetljo)
- add support for scsi media changers (svetljo)
- alsa 1.0.3 (svetljo)
  * update usx2y, msnd, pdplus patches
  * update to echoaudio 0.8.8rc1
  * add support for Intel8x0 and AMD768/8111 based modems
  * add support for RME Hammerfall DSP MADI soundcards
  * add support for ATI IXP 150/200/250 AC97 controller
- ieee1394 firewire rev 1181 (svetljo)
- update adaptec i2o dpt raid controllers (svetljo)
- add support for HP OmniBook (svetljo)
- update Permedia2 driver (svetljo)
- update ATI IXP IDE support (svetljo)
- fix matroxfb yres virtual (svetljo)
- add support for modular vesafb (svetljo)
- add support for tahoe 9xx serial cards (svetljo)
- add support for Berkshire Products USB-PC watchdog (svetljo)
- update video drivers: (svetljo)
  * cpia, v4l, bt832, tuner, bttv, saa7134, cx88, i2c, zoran
  * update documentation
- add saa5546a Teletext support (svetljo)
- update cifs to 1.04bk20040229 (svetljo)
- ext3 support for online resizing (svetljo)
- update hfs and add support for hfsplus (svetljo)
- update umsdos support (svetljo)
- add support for ufs2 filesystem (svetljo)
- update udf support (svetljo)
- update xfs support (svetljo)
- hostap 0.2.1 cvs 20040303 (svetljo)
- prism54 cvs 20040229 (svetljo)
- prism25 0.2.1-pre20 (svetljo)
- bcm5700 7.1.22 (svetljo)
- at76c503a 0.12Beta7 (svetljo)
- fuse 1.1 final (svetljo)
- usbvision 0.9.6 (svetljo)
- ogfs cvs20040302 (svetljo)
- Gatos ATI AIW capture driver (svetljo)
- cdfs 2.6.3 (svetljo)
- NOARP ARP filter 2.0.0 (svetljo)
- exaudio 1.58 (svetljo)
- updates and addons for device-mapper: (svetljo)
  * transparent device encryption
  * support mutipath hardware
  * snapshot, mirror, kcopycd support
  * bad block relocation support
  * evms support
  * lock fixes, bugfixes, updates...
- packet writing support (svetljo)
- add sysfs classes ppp, raw, vc (svetljo)
- add modular support to mce handler (svetljo)
- dbus over netlink socket support (svetljo)
- fix vc init race (svetljo)
- add support for Linux event logging (svetljo)
- mark mda console broken (svetljo)
- cloop 2.0.1 (svetljo)
- support IBM RAS Service processor (svetljo)
- add support for Cirrus PD6729 Compatible bridge support (svetljo)
- add support for IBM Power Linux RAID adapters (svetljo)
- add support for Swappiness Autoregulation (svetljo)
- add support for USB EPCAM Cameras (svetljo)
- acx100 0.2.0-pre7 + 20040219 updates and fixes (svetljo)
- spca5x video driver 20040228 (svetljo)
- quickcam-vc 1.0.7 (svetljo)
- fix Intel e1000 hang (svetljo)
- update dvb support: (svetljo)
  * docs, saa7134, skystar, frontends, stv0299, tda1004x, av7110, ttusb

* Sun Mar 07 2004 Thomas Backlund <tmb@mandrake.org> 2.6.3-4.tmb.2mdk
- quiet down atkbd warnings...
- require gcc 3.3.2-6mdk or newer since I build with -funit-at-a-time
- remove qla2xxx from 3rdparty as it's already in main kernel.org
  * move qla addons from 3rdparty to main scsi qla tree
- fix kdb kernel debugger (Douglas Wilkins)
  * minor -> MINOR
  * kdb belongs in kern_table, not in fs_table
- fix rmmod hang (svetljo)
- add support for mppe (svtljo)
- make quiet mode real quiet (svetljo)
- block ide-scsi for ide cdroms (svetljo)
- enable Silicon Image Serial ATA (svetljo)
- fix 3rdparty merge lost in sync with main (svetljo)

* Mon Mar 02 2004 Thomas Backlund <tmb@mandrake.org> 2.6.3-4.tmb.1mdk
- sync with main 2.6.3-4mdk
  * netfilter rtsp.
  * dcache security fix.
  * usb released wait on deregister bus.
  * usb-storage update.
  * ICH6 piix/libata support.
  * aacraid update.
  * sk98lin update.
  * mtp fusion update to 3.00.03.
  * ext3 fix access POSIX compiliant.
  * pm runtime deadlock fix.
  * sg direct io allowed as default.
  * bdclaim security oops fix.
  * blacklist Compaq ProLiant DL360 (acpi=off).
  * ipmi v30 (erwan request).
- fixed configs for alpha and sparc64 (Stefan)
-

* Tue Feb 24 2004 Thomas Backlund <tmb@mandrake.org> 2.6.3-2.tmb.1mdk
- sync with main 2.6.3-2mdk
  * bootsplash compil depend fix (chmou).
  * no more ide cdrom use ide-scsi.
  * fix libata pci quirks (remove 0x24d1).
  * parport updates.
  * enable ATM in BOOT kernel (tv request).
- a few fixes from alsa cvs
  * emu10k, ac97, cmipci

* Tue Feb 24 2004 Thomas Backlund <tmb@mandrake.org> 2.6.3-1.tmb.3mdk
- make sure scsi initio is built too
- add -funit-at-a-time back

* Sun Feb 22 2004 Thomas Backlund <tmb@mandrake.org> 2.6.3-1.tmb.2mdk
- fix bootsplash

* Sun Feb 22 2004 Thomas Backlund <tmb@mandrake.org> 2.6.3-1.tmb.1mdk
- fully synced with kernel-2.6.3.1mdk
- build i686-up-4GB kernel too
- i2c fixes
- add Asus P4B533-V to pci quirks

* Mon Feb 16 2004 Thomas Backlund <tmb@mandrake.org> 2.6.2-1.tmb.2mdk
- selected fixes from kernel-2.6.2.3mdk
  * pmpbios off by default
  * 8259 timer ack fix
  * selinux enforce node fix
  * xattr error checking fix
  * smb uid/gid permission fix
- modify alpha.config (stefan)
- disable ia64 support
- drop CP02_nforce2_disconnect_quirk
  * raises cpu temp about 6 degrees C according to acpi-devel ML :(
- drop CP03_nforce2_apic_io-edge_fix
  * does not work anymore
- redo CP05 for correct patches to mpparse on ix86 and amd64
- drop CA10_pcix-enhanced.patch
  * this is the one that breaks nforce2 systems
- drop DA20_sysfs-class-10-vc.patch
  * this still triggers the tty locking race (akpm)
- make sure kernel-source is readable by all (chmod -R a+rX)
- disable -funit-at-a-time for now, seems to break current gcc

* Sun Feb  8 2004 Thomas Backlund <tmb@mandrake.org> 2.6.2-1.tmb.1mdk
- fully synced with kernel-2.6.2.1mdk
- add 2.6.3-rc1 as a patch (so we don't change version)
  * includes alsa 1.0.2c
  * network fixes, netfilter fixes
  * sisfb updated
  * scsi fixes, aha152x fixes
  * + lots of other fixes...
- add sparc/sparc64 configs & fixes done on sparc.eijk.nu
- switch on smp and BOOT for sparc/sparc64
- add alpha configs & fixes done on alpha.eijk.nu
- switch on smp and BOOT for alpha
- modifications to lufs 0.9.7 (jaco)
  * Preserve LUFS filesystem uid/gid's if configured
  * Allow external links if configured
- usb pwc 9.0 beta1 (request by Warly)
- pci.ids 20040207tmb
- build i386 and amd64 with -funit-at-a-time if compiler supports it
- updated requirements for build / install:
  * module-init-tools >= 3.0-0.pre9.2mdk
  * modutils >= 2.4.26-3mdk
  * mkinitrd >= 3.5.18-3mdk
  * bootloader-utils >= 1.6-4mdk

* Wed Jan 28 2004 Thomas Backlund <tmb@mandrake.org> 2.6.2-0.rc2.1.tmb.2mdk
- fix pre/rc kernel versioning...
- redo DA10: alsa 1.0.2 patch
  * alsa developers reuploaded the tarball with a few fixes
    without other notice than the bugtracker :(
  * make sure we display correct alsa version: 1.0.2

* Tue Jan 27 2004 Thomas Backlund <tmb@mandrake.org> 2.6.2-0.rc2.1.tmb.1mdk
- 2.6.2-rc2
- alsa 1.0.2
- forcedeth 0.22
- squashfs 1.3r3
- pci.ids 20040125tmb
- sync with 2.6.2-0.rc1.1mdk
  * force inline memcmp when use Os (gb)
  * slim BOOT kernel.
  * ndis wrapper 0.4.
  * acpi 20031203.
  * raid6 20040107.
  * nfs/nfsd updates.

* Wed Jan 20 2004 Thomas Backlund <tmb@mandrake.org> 2.6.1-1.tmb.10mdk
- argh... me sucks... agp stuff should stay as modules

* Tue Jan 20 2004 Thomas Backlund <tmb@mandrake.org> 2.6.1-1.tmb.9mdk
- 2.6.1-bk6
- sync with -mm5
- dropped ramdisk leak patches CF03, CF04 (mm5: was wrong)
- dropped DA32_ide-siimage-stack-fix (mm5: needs to be reworked)
- dropped ppc64 fixes CB01-CB07 (merged upstream)
- dropped CF01, CF02, DA33, DA41, DF02, DF03, DN21 (merged upstream)
- dropped remove_CardServices DO01 - DO07 (merged upstream)
- dropped v4l patches DV21-DV30 (merged upstream)
- dropped ext2/3 fixes FE01-FE04, xfs FX01 (merged upstream)
- dropped BA01, BA03, BI03, FA05, FJ01, ME01, ME02 (merged upstream)
- dropped acpi CE05-CE08, kdb CK01-CK03, CM01, CM03 (merged upstream)
- dropped sysfs patches MS01-MS05, MS07-MS09 (merged upstream)
- resync DA10_alsa_1.0.1, DA22_alsa_bt87x
- resync DC01 pci.ids.tmb
- resync FA04_invalidate_inodes-speedup
- resync FA08_O_DIRECT-race-fixes-rollup
- CA02: define MAX_INIT_ARGS/ENVS 32 to support more kernel args (Jaco)
- FS01: upgrade supermount-ng to 2.0.4-2.6.1

* Mon Jan 19 2004 Thomas Backlund <tmb@mandrake.org> 2.6.1-1.tmb.8mdk
- 2.6.1-bk4
- drop patches: (merged upstream)
  * DA01-DA07, DA19, DA36-DA38, DF05
- resynced patches DV01-DV16 and moved to DV20-DV30 (v4l)
- make some more drivers modules instead of builtin...
- from -mm4:
  * update libata 0.52
  * pcmcia CardService updates
  * sysfs support
  * readd alsa sysfs
  * md blockdevice fixes
  * restore HT detection algoritm
  * ramdisk and fixes and cleanup
  * ali m1533 dma hang fix
  * change BUG to BUG_ON calls for code speedup
  * laptop mode support
  * fix msi megaraid id
  * fix keyboard scancode to keep 2.4 compability
  * fix kernel-locking doc tmplate
- scsi aic79xx 20031222 (svetljo)
- cifs 1.00 (svetljo)
- 3rdparty qc-usb 0.6.0 (svetljo)

* Tue Jan 13 2004 Thomas Backlund <tmb@mandrake.org> 2.6.1-1.tmb.7mdk
- fix changelog for 5mdk
- add initial support more arches
  * alpha, ia64, x86_64, sparc, sparc64
  * add configs for all above (based on 2.6.1 defconfigs)
  * enable them in the scripts
  * please tell me what you want changed in the configs,
    as I don't have the h/w myself...
- drop loop related patches DB21-DB27 gotten from -mm as they 
  are broken (svetljo)
- gzip modules to minimize needed space for installed kernel
- make apm support builtin, not as module

* Mon Jan 12 2004 Thomas Backlund <tmb@mandrake.org> 2.6.1-1.tmb.6mdk
- back out drm/dri 20040107cvs (seems to cause xfree hangs)
- fix changelog typos for 1mdk to 4mdk

* Sun Jan 11 2004 Thomas Backlund <tmb@mandrake.org> 2.6.1-1.tmb.5mdk
- drop pnp-fix-1, makes kernel oops with Bad EIP (svetljo)
- dont depend on udev and sysfsutils, atleast for now (svetljo)

* Sun Jan 11 2004 Thomas Backlund <tmb@mandrake.org> 2.6.1-1.tmb.4mdk
- keep BLK_DEV_MD builtin, not as a module

* Sun Jan 11 2004 Thomas Backlund <tmb@mandrake.org> 2.6.1-1.tmb.3mdk
- another quick fix... (me sux again :-()
- fix 3rdparty config... (svetljo)
- fix unpackaged files
- disable BLK_DEV_IDEPNP
- sync some more of the configs from kernel-2.6 in contribs

* Sat Jan 10 2004 Thomas Backlund <tmb@mandrake.org> 2.6.1-1.tmb.2mdk
- bugfix for broken sound, me sux :-(
- drop the alsa sysfs patch until all sysfs patches are added...

* Sat Jan 10 2004 Thomas Backlund <tmb@mandrake.org> 2.6.1-1.tmb.1mdk
- 2.6.1
- add --with nosrc option to build nosrc.rpm
- fix typo in description (jaco)
- disable CONFIG_REISERFS_CHECK
- disable IEEE1394_OUI_DB
- disable MTD_DOC2000 (wont build)
- build agp drivers as modules
- dropped a lot of patches (merged upstream):
  * CA09-CA11, CA13, CA15, CA17, CA19-CA24, CA27-CA28, CA35, CA37-CA40,
  * CA43-CA44, CB10, CC01, CI01, CM04-CM09, CS01, DA04, DA11-DA12, 
  * DA16, DA18, DA21-DA22, DB01-DB04, DB16-DB23, DF03, DI01-DI02,
  * DM01-DM02, DN01, DN05, DP01, DS01, DU01, DV13-DV14, FA01, FA03,
  * FA07, FA09, FE01-FE03, FQ01 
- dropped patches that needs verification:
  * CA08, CA12, CA14, CA33, CA36, CB11-CB12, DA15, DA20, 
  * DB05-DB06, DB08
- rediffed patches:
  * DS02, DV02
- replaced patches with newer ones:
  * DB09-DB14 replaced with DB21-DB27 (from mm1)
  * DA17 with DA37-DA38
- forcedeth 0.20
- pci.ids 20040109tmb
- supermount-ng 2.0.3a
- ieee1394 rev 1092
  * typos fixed, updated oui.db
- ext2 / ext3 fixes (from mm1)
  * inode fixes, debug fixes, next generation fixes
- libata sata_sil 0.52 updates (from mm1) 
  * support 3114, add another 3112 model (from mm1)
- add support for radeon Yd (from mm1)
- drm/dri 20040107 cvs (from mm1)
- NetGear FA311 mac byte swap address fix (from mm1)
- scsi fixes (from mm1)
  * inia100 fixes
  * qla1280 fixes
- misc fixes (from mm1)
  * rmmod race fix
  * rtc leak fix
  * vc init race fix
- nforce2 fixes for disconnect_quirk, io_apic edge (svetljo)
- alsa 1.0.1 (from mm1)
- alsa 1.0.1 addons (svetljo)
  * nforce 3 support
  * add sysfs class
  * aureal/vortex/vortex2
  * usx2y, pdplus, mixart, msnd, pdaudio, bt87x
  * echoaudio 0.8.3
- hpt374 autotune fix (svetljo)
- 3rparty drivers (svetljo)
  * bcm5700 7.1.9
  * bcm4400 3.0.7
  * qla2xxx-8.00.00b8
  * ivtv-281103cvs
  * hfsplus_20030930
  * viahss-0.92
  * ogfs
  * w9968cf-1.24
  * vt_ar5k-20030509
  * fuse-1.1_pre1
  * airo_mpi-20031220
  * svgalib_helper-1.9.18
- 3rdparty Makefile, Kconfig, misc fixes (svetljo)

* Thu Jan  1 2004 Thomas Backund <tmb@mandrake.org> 2.6.0-1.tmb.1mdk
- first kernel-tmb based on 2.6.0 final made by Nicholas
- squashfs 1.3r2
- pci.ids 2003-12-09 + my addons
- use some specfile and scripts magic from Juans 2.4.spec
- fix postun macros
- merge changes from contrib kernel-2.6-2.6.0-1mdk
  * thanks to Oliver Blin and Oliver Thauvin for their great work
  * keep preemptive and cramfs buitin for now...
  * supermount 2.0.3

* Thu Dec 18 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.0-1mdk
- 2.6.0 final version ;)
- ndis wrapper 0.3.
- fix uss725.

* Wed Dec 17 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.0-0.5mdk
- bk13.
- acecad 1.3.
- uss725.
- bttv videodev i2c videobuf updates 20031216.
- dvb timeout fix.
- mod_marvel (Kevin O'Connor).
- matrox_fb fixes (Kevin O'Connor).
- forcedeth v19.
- kdb build fix.
- add siimage 3114 support.
- prism25 0.2.1-pre16.
- qc-usb cvs20031216.

* Fri Dec 12 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.0-0.4mdk
- bk8.
- add vt|ar5k wireless chipset support.
- dos partition table consistency.
- warly touch boot logo ;)
- ndis wrapper 0.2. (only for up kernel)
- alsa 1.0.0rc2.
- agpgart and mousedev as built-in.

* Thu Dec 04 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.0-0.3mdk
- bk1:
  * ide-scsi.c uninitialized variable
  * x86 kernel page fault error codes
  * lost wakeups problem
  * missing initialization of /proc/net/tcp seq_file
- rework merge version.h (now all kernel have UTS_RELEASE defined)
- 2.6.0-test11q2 :
  * libata update
  * pwc 8.12
  * prism54 cvs20031203
  * alsa 1.0.0rc1

* Fri Nov 28 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.0-0.2mdk
- re-support on the fly module building (great for properitary packages)
- 2.6.0-test11q2 :
  * lots of mm patches
  * import somes 3rdparty and patches : (svetoslav)
    * lirc
    * at76c503a
    * bcm5700
    * dfg1394
    * dxr3
    * iscsi-mod
    * lufs
    * ov511
    * prism25
    * prism54
    * qc-usb

* Mon Nov 24 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.6.0-0.1mdk
- First version to move on kernel-2.6.0. (aka: ready for a new age).
- 2.6.0-test10q1 :
  * only i386 config for the moment
  * bootsplash 3.1.3
  * mdk logo
  * forcedeth v18
  * adiusbadsl 1.0.4 (untested)
  * acx100 0.2.0pre6
  * hostap 0.1.2

# Local Variables:
# rpm-spec-insert-changelog-version-with-shell: t
# End:
