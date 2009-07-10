#
# *tmb* series kernels now use kernel.org versioning
#
%define kernelversion	2
%define patchlevel	6
%define sublevel	31

# kernel Makefile extraversion is substituted by 
# kpatch/kgit/kstable wich are either 0 (empty), rc (kpatch), 
# git (kgit, only the number after "git"), or stable release (kstable)
%define kpatch		rc2
%define kgit		4
%define kstable		0

# this is the releaseversion
%define kbuild		1

%define ktag 		tmb
%define kname 		kernel-%{ktag}

%define rpmtag		%distsuffix
%if %kpatch
%if %kgit
%define rpmrel		%mkrel 0.%{kpatch}.%{kgit}.%{kbuild}
%else
%define rpmrel		%mkrel 0.%{kpatch}.%{kbuild}
%endif
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
%if %kgit
%define buildrpmrel     0.%{kpatch}.%{kgit}.%{kbuild}%{rpmtag}
%else
%define buildrpmrel     0.%{kpatch}.%{kbuild}%{rpmtag}
%endif
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

# Build mm (i686 / 4GB) / x86_64
%define build_desktop		1

# Build laptop (i686 / 4GB)/ x86_64
%ifarch %{ix86} x86_64
%define build_laptop		1
%endif

# Build realtime (i686 / 4GB)/x86_64
%define build_realtime		0

# Build server (i686 / 64GB)/x86_64
%define build_server		1

# End of user definitions
%{?_without_desktop586: %global build_desktop586 0}
%{?_without_desktop: %global build_desktop 0}
%{?_without_laptop: %global build_laptop 0}
%{?_without_realtime: %global build_realtime 0}
%{?_without_server: %global build_server 0}
%{?_without_doc: %global build_doc 0}
%{?_without_source: %global build_source 0}
%{?_without_devel: %global build_devel 0}
%{?_without_debug: %global build_debug 0}

%{?_with_desktop586: %global build_desktop586 1}
%{?_with_desktop: %global build_desktop 1}
%{?_with_laptop: %global build_laptop 1}
%{?_with_realtime: %global build_realtime 1}
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

# Parallelize xargs invocations on smp machines
%define kxargs xargs %([ -z "$RPM_BUILD_NCPUS" ] \\\
	&& RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"; \\\
	[ "$RPM_BUILD_NCPUS" -gt 1 ] && echo "-P $RPM_BUILD_NCPUS")

#
# SRC RPM description
#
Summary: 	Linux kernel built for Mandriva with modifications by %{ktag}
Name:		%{kname}
Version: 	%{kversion}
Release: 	%{rpmrel}
License: 	GPLv2
Group: 	 	System/Kernel and hardware
ExclusiveArch: 	%{ix86} x86_64
ExclusiveOS: 	Linux
URL: 		http://wiki.mandriva.com/en/Docs/Howto/Mandriva_Kernels#kernel-tmb

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
# This is for disabling mrproper in -devel rpms
Source2: 	disable-mrproper-in-devel-rpms.patch
# This is for disabling the rest of the scripts in -devel rpms
Source3:	disable-prepare-scripts-configs-in-devel-rpms.patch

Source4: 	README.kernel-%{ktag}-sources
Source5: 	README.Mandriva_Linux_%{ktag}

# This is for keeping asm-offsets.h and bounds.h in -devel rpms
Source6: 	kbuild-really-dont-remove-bounds-asm-offsets-headers.patch

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
%if %kgit
Patch2:		ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/snapshots/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}-git%{kgit}.bz2
Source11:	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/snapshots/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}-git%{kgit}.bz2.sign
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
http://www.mandriva.com/en/security/kernelupdate			\
									\
The %{ktag} kernels is an experimental kernel based on the kernel.org	\
kernels with added patches. Some of them may/will never end up in	\
the main kernels due to their experimental nature. Some refer to	\
this kernel as a 'hackkernel' ...					\
Use these kernels at your own risk !!					

### Global Requires/Provides
%define requires1 	mkinitrd >= 4.2.17-%mkrel 52
%define requires2 	bootloader-utils >= 1.12-%mkrel 1
%define requires3 	sysfsutils >= 1.3.0-%mkrel 1 module-init-tools >= 3.2-0.pre8.%mkrel 2
%define requires4	kernel-firmware >= 2.6.27-1mmb

%define kprovides 	%{kname} = %{kverrel}, kernel = %{tar_ver}, drbd-api = 88

BuildRoot: 		%{_tmppath}/%{kname}-%{kversion}-%{_arch}-build
%define buildroot	%{_tmppath}/%{kname}-%{kversion}-%{_arch}-build
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
Provides:	should-restart = system			\
Requires(pre):	%requires1 %requires2 %requires3 %requires4 \
%ifarch %{ix86}						\
Conflicts:	arch(x86_64)				\
%endif							\
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
%ifarch %{ix86}						\
Conflicts:	arch(x86_64)				\
%endif							\
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
%ifarch %{ix86}						\
Conflicts:	arch(x86_64)				\
%endif							\
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
%ifarch %{ix86}						\
Conflicts:	arch(x86_64)				\
%endif							\
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
# kernel-desktop586: i586, smp-alternatives, 4GB
#

%if %build_desktop586
%define summary_desktop586 Linux kernel for desktop use with i586 & 4GB RAM
%define info_desktop586 This kernel is compiled for desktop use, single or \
multiple i586 processor(s)/core(s) and less than 4GB RAM, using full \
preempt, CFS cpu scheduler and cfq i/o scheduler. \
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
multiple i686 processor(s)/core(s) and less than 4GB RAM, using full \
preempt, CFS cpu scheduler and cfq i/o scheduler. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%else
%define summary_desktop Linux Kernel for desktop use with %{_arch}
%define info_desktop This kernel is compiled for desktop use, single or \
multiple %{_arch} processor(s)/core(s), using full preempt, CFS cpu \
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
multiple i686 processor(s)/core(s) and less than 4GB RAM, using HZ_250 \
to save battery, voluntary preempt, CFS cpu scheduler, cfq i/o scheduler \
and some other laptop-specific optimizations. If you want to sacrifice \
battery life for performance, you better use the %{kname}-desktop. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter. \
NOTE! This kernel also uses TuxOnIce by default.
%else
%define summary_laptop Linux kernel for laptop use with %{_arch}
%define info_laptop This kernel is compiled for laptop use, single or \
multiple %{_arch} processor(s)/core(s), using HZ_250 to save battery, \
voluntary preempt, CFS cpu scheduler, cfq i/o scheduler and some other \
laptop-specific optimizations. If you want to sacrifice battery life for \
performance, you better use the %{kname}-desktop. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter. \
NOTE! This kernel also uses TuxOnIce by default.
%endif
%mkflavour laptop
%endif

%if %build_realtime
%ifarch %{ix86}
%define summary_realtime Linux Kernel for desktop use with i686 & 4GB RAM
%define info_realtime This kernel is compiled for desktop use, single or \
multiple i686 processor(s)/core(s) and less than 4GB RAM, using full \
preempt and realtime, CFS cpu scheduler and cfq i/o scheduler. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%else
%define summary_realtime Linux Kernel for desktop use with %{_arch}
%define info_realtime This kernel is compiled for desktop use, single or \
multiple %{_arch} processor(s)/core(s), using full preempt and realtime, \
CFS cpu scheduler and cfq i/o scheduler. \
This kernel relies on in-kernel smp alternatives to switch between up & smp \
mode depending on detected hardware. To force the kernel to boot in single \
processor mode, use the "nosmp" boot parameter.
%endif
%mkflavour realtime
%endif

#
# kernel-server: i686, smp-alternatives, 64 GB /x86_64
#

%if %build_server
%ifarch %{ix86}
%define summary_server Linux Kernel for server use with i686 & 64GB RAM
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
Provides: 	kernel-source = %{kverrel}, kernel-devel = %{kverrel}
%ifarch %{ix86}
Conflicts:	arch(x86_64)
%endif

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
		if [ ! -L $i/build -a ! -L $i/source ]; then	
            		ln -sf /usr/src/%{kversion}-%{ktag}-%{buildrpmrel} $i/build
            		ln -sf /usr/src/%{kversion}-%{ktag}-%{buildrpmrel} $i/source
		fi
        fi
done

%preun -n %{kname}-source-%{buildrel}
for i in /lib/modules/%{kversion}-%{ktag}-*-%{buildrpmrel}/{build,source}; do
	if [ -L $i ]; then
		if [ "$(readlink $i)" = "/usr/src/%{kversion}-%{ktag}-%{buildrpmrel}" ]; then
			rm -f $i
		fi
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
%ifarch %{ix86}
Conflicts:	arch(x86_64)
%endif

%description -n %{kname}-source-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-source installed...

%common_description_info

#
# kernel-doc: documentation for the Linux kernel
#
%if %build_doc
%package -n %{kname}-doc
Version: 	%{kversion}
Release: 	%{rpmrel}
Summary: 	Various documentation bits found in the %{kname} source
Group: 		Books/Computer books

%description -n %{kname}-doc
This package contains documentation files from the %{kname} source. 
Various bits of information about the Linux kernel and the device drivers 
shipped with it are documented in these files. You also might want install 
this package if you need a reference to the options that can be passed to 
Linux kernel modules at load time.

%common_description_info
%endif #build_doc
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
%if %kgit
%patch2 -p1
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

%{patches_dir}/scripts/create_configs %debug --user_cpu="%{_arch}"

# make sure the kernel has the sublevel we know it has...
LC_ALL=C perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{sublevel}/" Makefile

# get rid of unwanted files
find . -name '*~' -o -name '*.orig' -o -name '*.append' |%kxargs rm -f


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

	if [ -z "$name" ]; then
		cp arch/x86/configs/%{_arch}_defconfig-desktop .config
	else
		cp arch/x86/configs/%{_arch}_defconfig-$name .config
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

	cp -f arch/%{_arch}/boot/bzImage %{temp_boot}/vmlinuz-$KernelVer

	# modules
	install -d %{temp_modules}/$KernelVer
	%smake INSTALL_MOD_PATH=%{temp_root} KERNELRELEASE=$KernelVer modules_install 

	# remove /lib/firmware, we use a separate kernel-firmware
	rm -rf %{temp_root}/lib/firmware
}


SaveDevel() {
	devel_flavour=$1

	DevelRoot=/usr/src/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}
	TempDevelRoot=%{temp_root}$DevelRoot

	mkdir -p $TempDevelRoot
	for i in $(find . -name 'Makefile*'); do cp -R --parents $i $TempDevelRoot;done
	for i in $(find . -name 'Kconfig*' -o -name 'Kbuild*'); do cp -R --parents $i $TempDevelRoot;done
	cp -fR include $TempDevelRoot
	cp -fR scripts $TempDevelRoot
	%ifarch %{ix86} x86_64
		cp -fR arch/x86/kernel/asm-offsets.{c,s} $TempDevelRoot/arch/x86/kernel/
		cp -fR arch/x86/kernel/asm-offsets_{32,64}.c $TempDevelRoot/arch/x86/kernel/
		cp -fR arch/x86/include $TempDevelRoot/arch/x86/
	%else
		cp -fR arch/%{_arch}/kernel/asm-offsets.{c,s} $TempDevelRoot/arch/%{_arch}/kernel/
		cp -fR arch/%{_arch}/include $TempDevelRoot/arch/%{_arch}/
	%endif
	cp -fR kernel/bounds.c $TempDevelRoot/kernel/
	cp -fR .config Module.symvers $TempDevelRoot
	cp -fR 3rdparty/mkbuild.pl $TempDevelRoot/3rdparty/

	# Needed for truecrypt build (Danny)
	cp -fR drivers/md/dm.h $TempDevelRoot/drivers/md/

	# Needed for lguest
	cp -fR drivers/lguest/lg.h $TempDevelRoot/drivers/lguest/

	# Needed for lirc_gpio (Anssi Hannula, #39004)
	cp -fR drivers/media/video/bt8xx/bttv{,p}.h $TempDevelRoot/drivers/media/video/bt8xx/

	# Needed for external dvb tree (#41418)
	cp -fR drivers/media/dvb/dvb-core/*.h $TempDevelRoot/drivers/media/dvb/dvb-core/
	cp -fR drivers/media/dvb/frontends/lgdt330x.h $TempDevelRoot/drivers/media/dvb/frontends/

	# add acpica header files, needed for fglrx build
	cp -fR drivers/acpi/acpica/*.h $TempDevelRoot/drivers/acpi/acpica/

	for i in alpha arm arm26 avr32 blackfin cris frv h8300 ia64 microblaze mips m32r m68k \
		 m68knommu mn10300 parisc powerpc ppc s390 sh sh64 sparc v850 xtensa; do
		rm -rf $TempDevelRoot/arch/$i
		rm -rf $TempDevelRoot/include/asm-$i
	done

	%ifnarch %{ix86} x86_64
		rm -rf $TempDevelRoot/arch/x86
		rm -rf $TempDevelRoot/include/asm-x86
	%endif
	# disable removal of asm-offsets.h and bounds.h
	patch -p1 -d $TempDevelRoot -i %{SOURCE6}

	# Clean the scripts tree, and make sure everything is ok (sanity check)
	# running prepare+scripts (tree was already "prepared" in build)
	pushd $TempDevelRoot >/dev/null
		%smake -s prepare scripts clean
	popd >/dev/null

	rm -f $TempDevelRoot/.config.old

	# fix permissions
	chmod -R a+rX $TempDevelRoot

	# disable mrproper in -devel rpms
	patch -p1 -d $TempDevelRoot -i %{SOURCE2}
	# disable the rest of the scripts in -devel rpms
	patch -p1 -d $TempDevelRoot -i %{SOURCE3}

	kernel_devel_files=../kernel_devel_files.$devel_flavour


### Create the kernel_devel_files.*
cat > $kernel_devel_files <<EOF
%defattr(-,root,root)
%dir $DevelRoot
%dir $DevelRoot/arch
%dir $DevelRoot/include
$DevelRoot/3rdparty
$DevelRoot/Documentation
$DevelRoot/arch/Kconfig
$DevelRoot/arch/um
%ifarch %{ix86} x86_64
$DevelRoot/arch/x86
%endif
$DevelRoot/block
$DevelRoot/crypto
$DevelRoot/drivers
$DevelRoot/firmware
$DevelRoot/fs
$DevelRoot/include/Kbuild
$DevelRoot/include/acpi
$DevelRoot/include/asm
$DevelRoot/include/asm-generic
%ifarch %{ix86} x86_64
$DevelRoot/include/asm-x86
%endif
$DevelRoot/include/config
$DevelRoot/include/crypto
$DevelRoot/include/drm
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
$DevelRoot/include/trace
$DevelRoot/include/video
$DevelRoot/include/xen
$DevelRoot/init
$DevelRoot/ipc
$DevelRoot/kernel
$DevelRoot/lib
$DevelRoot/mm
$DevelRoot/net
$DevelRoot/samples
$DevelRoot/scripts
$DevelRoot/security
$DevelRoot/sound
$DevelRoot/tools
$DevelRoot/usr
$DevelRoot/.config
$DevelRoot/Kbuild
$DevelRoot/Makefile
$DevelRoot/Module.symvers
%doc README.Mandriva_Linux_%{ktag}
%doc README.kernel-%{ktag}-sources
EOF


### Create -devel Post script on the fly
cat > $kernel_devel_files-post <<EOF
if [ -d /lib/modules/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel} ]; then
	rm -f /lib/modules/%{kversion}-%{ktag}-$devel_flavour-%{buildrpmrel}/{build,source}
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
# create kernel-devel symlinks if matching -devel- rpm is installed
if [ -d /usr/src/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel} ]; then
	rm -f /lib/modules/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}/{build,source}
	ln -sf /usr/src/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel} /lib/modules/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}/build
	ln -sf /usr/src/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel} /lib/modules/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}/source
fi
%endif
%if %build_source
# create kernel-source symlinks only if matching -devel- rpm is not installed
if [ -d /usr/src/%{kversion}-%{ktag}-%{buildrpmrel} -a ! -d /usr/src/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel} ]; then
	rm -f /lib/modules/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}/{build,source}
	ln -sf /usr/src/%{kversion}-%{ktag}-%{buildrpmrel} /lib/modules/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}/build
	ln -sf /usr/src/%{kversion}-%{ktag}-%{buildrpmrel} /lib/modules/%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}/source
fi
%endif
EOF


### Create kernel Preun script on the fly
cat > $kernel_files-preun <<EOF
/sbin/installkernel -R %{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}
pushd /boot > /dev/null
if [ -L vmlinuz-%{ktag}-$kernel_flavour ]; then
	if [ "$(readlink vmlinuz-%{ktag}-$kernel_flavour)" = "vmlinuz-%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}" ]; then
		rm -f vmlinuz-%{ktag}-$kernel_flavour
	fi
fi
if [ -L initrd-%{ktag}-$kernel_flavour.img ]; then
	if [ "$(readlink initrd-%{ktag}-$kernel_flavour.img)" = "initrd-%{kversion}-%{ktag}-$kernel_flavour-%{buildrpmrel}.img" ]; then
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

%if %build_realtime
CreateKernel realtime
%endif

%if %build_server
CreateKernel server
%endif


# kernel-source is shipped as a clean source tree, with no preparation
%if %build_source
    PrepareKernel "" %{buildrpmrel}%{ktag}custom
%smake -s mrproper
%endif


###
### install
###
%install
install -m 644 %{SOURCE4}  .
install -m 644 %{SOURCE5}  .

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
for i in alpha arm arm26 avr32 blackfin cris frv h8300 ia64 microblaze mips m32r m68k \
	 m68knommu mn10300 parisc powerpc ppc s390 sh sh64 sparc v850 xtensa; do
	rm -rf %{target_source}/arch/$i
	rm -rf %{target_source}/include/asm-$i
done

%ifnarch %{ix86} x86_64
	rm -rf %{target_source}/arch/x86
	rm -rf %{target_source}/include/asm-x86
%endif

# other misc files
rm -f %{target_source}/{.config.old,.config.cmd,.mailmap,.missing-syscalls.d,arch/.gitignore}

#endif %build_source
%endif

# gzipping modules
find %{target_modules} -name "*.ko" | %kxargs gzip -9

# We used to have a copy of PrepareKernel here
# Now, we make sure that the thing in the linux dir is what we want it to be
for i in %{target_modules}/*; do
    rm -f $i/build $i/source
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
	echo $modules | %kxargs /sbin/modinfo \
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
%{_kerneldir}/arch/Kconfig
%{_kerneldir}/arch/um
%ifarch %{ix86} x86_64
%{_kerneldir}/arch/x86
%endif
%{_kerneldir}/block
%{_kerneldir}/crypto
%{_kerneldir}/drivers
%{_kerneldir}/firmware
%{_kerneldir}/fs
%{_kerneldir}/include/Kbuild
%{_kerneldir}/include/acpi
%{_kerneldir}/include/asm-generic
%ifarch %{ix86} x86_64
%{_kerneldir}/include/asm-x86
%endif
%{_kerneldir}/include/crypto
%{_kerneldir}/include/drm
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
%{_kerneldir}/include/trace
%{_kerneldir}/include/video
%{_kerneldir}/include/xen
%{_kerneldir}/init
%{_kerneldir}/ipc
%{_kerneldir}/kernel
%{_kerneldir}/lib
%{_kerneldir}/mm
%{_kerneldir}/net
%{_kerneldir}/samples
%{_kerneldir}/scripts
%{_kerneldir}/security
%{_kerneldir}/sound
%{_kerneldir}/tools
%{_kerneldir}/usr
%{_kerneldir}/virt
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
#endif build_source

%files -n %{kname}-source-latest
%defattr(-,root,root)

%endif

%if %build_doc
%files -n %{kname}-doc
%defattr(-,root,root)
%doc linux-%{tar_ver}/Documentation/*
%endif

%changelog
* Fri Jul 10 2009 Thomas Backlund <tmb@mandriva.org> 2.6.31-0.rc2.4.1mdv
- update to 2.6.31-rc2-git4
- drop patches merged upstream:
    * DC01: avoid oom lockup on /dev/zero
    * DG06-DG26: drm updates
    * DH15: asus hwmon atk0110 support
    * DH20: wacom bluetooth support
    * DI10: wacom intuos4 support
    * DN16: r8169: use family-specific defaults for unknown chips
    * DS02: Alsa buildfixes
    * DU01: qcserial support
    * FN01: nfsd: report short writes
    * FS15: ext4: Avoid corrupting the uninitialized bit in the extent 
	    during truncate
- update patches:
    * DG02: drm: nouveau (rh 2.6.31-0.42.rc2.fc12)
    * DG03: drm: no gem on i8xx (rh 2.6.31-0.42.rc2.fc12)
    * DG04: drm: i915 resume force mode (rh 2.6.31-0.42.rc2.fc12)
    * DG05: drm: intel big hammer (rh 2.6.31-0.42.rc2.fc12)
    * DI01: input: lirc (rh 2.6.31-0.42.rc2.fc12)
    * CE02: Acpi DSDT support (from main)
    * DM50: v4l-dvb snapshot 2009-07-09
    * DS01: Alsa 1.0.20+ snapshot 2009-07-09
    * FR01: Reiser4 support
    * MB10-MB13: Ndiswrapper 1.55 (from main)
    * MC30-MC34: Drbd 8.3.2 (from main)
- drop unneeded patches:
    * DN01: bonding module alias
    * DN10: net: revert forcedeth power down phy when interface is down
    * DS04: sound: usb-gadget gmidi buildfix with updated alsa
- disable broken patches:
    * DG00: drm: drm-next
    * DG01: drm: radeon modesetting
    * FS01: unionfs 2.5.2
    * KP01: tuxonice 3.0.1
    * MM01: saner vm settings
- update defconfigs

* Fri Jul  3 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.6-1mdv
- update to 2.6.29.6
- update patches:
    * DM50: v4l-dvb snapshot 2009-07-03
    * DM51: v4l-dvb snapshot 2009-07-03 buildfix
    * DS01: Alsa 1.0.20+ snapshot 2009-07-03
    * DS02: Alsa 1.0.20+ snapshot 2009-07-03 buildfix
    * DS10: Alsa 1.0.20+ unstable 2009-07-03 via-vt1732
- add patches:
    * DS11: Alsa 1.0.20+ unstable 2009-07-03 cirrus-cs420x
- drop patches merged upstream:
    * DN15: net: r8169: fix crash when large packets are received
    * FS10: fs: jbd: fix race in buffer processing in commit code
- re-enable in 64bit server kernels:
    * NUMA, K8_NUMA, X86_64_ACPI_NUMA, NODES_SPAN_OTHER_NODES
    * NODES_SHIFT=6, NEED_MULTIPLE_NODES, MIGRATION
    * HAVE_ARCH_EARLY_PFN_TO_NID, ACPI_NUMA
- update defconfigs

* Fri Jun 26 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.5-3mdv
- reenable in defconfigs:
    * TASKSTATS, TASK_DELAY_ACCT, TASK_XACCT, TASK_IO_ACCOUNTING
    * AUDIT, AUDITSYSCALL, AUDIT_TREE, AUDIT_GENERIC

* Mon Jun 22 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.5-2mdv
- full resync of drm with Fedora 2.6.29.5-191.fc11:
    * DG00: drm-next
    * DG01: drm modesetting radeon
    * DG02: drm nouveau
    * DG03: drm no gem on i8xx
    * DG04: drm i915 resume force mode
    * DG05: drm intel big hammer
    * DG06: drm intel lying systems without lvds
    * DG07: drm intel gen3 fb hack
    * DG08: drm intel hdmi edid fix
    * DG09: drm intel tiling transition
    * DG10: drm intel next
    * DG11: drm intel debugfs ringbuffer
    * DG12: drm edid ignore tiny modes
    * DG13: drm intel include 965gme pci id
    * DG14: drm intel gem use dma32 on pae
    * DG15: drm intel i8xx cursors
    * DG16: drm intel vmalloc
    * DG17: drm copyback ioctl data to userspace regardless of retcode
    * DG18: drm i915 apply a big hammer to 865 gem object
    * DG19: drm i915 fix tiling pitch
    * DG20: drm intel set domain on fault
    * DG21: drm modesetting radeon fixes
    * DG22: drm radeon fix ring commit
    * DG23: drm radeon new pciids (RV740)
    * DG24: drm dont frob i2c
    * DG25: drm connector dpms fix
    * DG26: drm intel tv fix
- add patches:
    * DC01: avoid lockup on OOM with /dev/zero
    * DN16: r8169: use family-specific defaults for unknown chips
    * FN01: nfsd: report short writes count to the client
    * MM01: set saner vm settings: raise default dirty level, lower swappiness
- Disable COMEDI_PCI_DRIVERS. At least one module built with  it enabled 
  (s626) claims the pci id 1131:7146 for all subvendors and subdevice ids.
  The problem is that this will clash with many media/dvb cards. (#51314)

* Thu Jun 18 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.5-1mdv
- update to 2.6.29.5 (CVE-2009-1630, CVE-2009-1385)
- drop patches merged upstream:
    * AA01: 2.6.29.5-rc1
- add patches:
    * FS15: ext4: Avoid corrupting the uninitialized bit in the extent
	    during truncate
- update patches:
    * DM50: v4l-dvb snapshot 2009-06-18
    * DS01: Alsa 1.0.20+ snapshot 2009-06-18
    * DS02: ALsa snapshot buildfix
    * DS10: Alsa 1.0.20+ unstable addon: via vt1732 (Envy24-II)
    * FS01: unionfs 2.5.2
- rediff patches:
    * DS05: add Toshiba Pro A210 to quirk table
- update defconfigs

* Wed Jun 10 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.4-7mdv
- add patches:
    * DN15: net: r8169: fix crash when large packets are received
    * FS10: fs: jbd: fix race in buffer processing in commit code
- more defconfig optimizations:
    * disable in defconfigs:
	* DETECT_SOFTLOCKUP, EARLY_PRINTK, SCHED_DEBUG, SCHEDSTATS, TIMER_STATS
	* JFS_STATISTICS, OCFS2_FS_STATS, CIFS_STATS
    * enable in defconfigs:
	* SND_HDA_RECONFIG, INTR_REMAP

* Tue Jun  9 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.4-6mdv
- more defconfig optimizations:
    * disable in defconfigs:
	* AUDIT, AUDITSYSCALL, AUDIT_TREE, AUDIT_GENERIC
	* PARAVIRT_GUEST, VMI, KVM_CLOCK, KVM_GUEST, LGUEST_GUEST
    	* PARAVIRT, PARAVIRT_CLOCK, NETLABEL, NETFILTER_DEBUG
	* IP_NF_SECURITY, IP6_NF_SECURITY, IWLWIFI_DEBUG, IWL3945_DEBUG
	* HISAX_DEBUG, SECURITY, SECURITY_NETWORK, SECURITY_NETWORK_XFRM
	* SECURITY_PATH, SECURITY_FILE_CAPABILITIES, SECURITY_DEFAULT_MMAP_MIN_ADDR
	* NUMA, K8_NUMA, X86_64_ACPI_NUMA, NODES_SPAN_OTHER_NODES, NODES_SHIFT
	* NEED_MULTIPLE_NODES, MIGRATION, HAVE_ARCH_EARLY_PFN_TO_NID, ACPI_NUMA
    *  enable in defconfigs:
	* JFS_SECURITY, DIRECT_GBPAGES

* Tue Jun  9 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.4-5mdv
- add patches:
    * AA00: 2.6.29.5-rc1
    * LG01: add note about latencytop bloat in Kconfig.debug
- drop patches merged upstream:
    * AA01-AA27: Stable Queue patches
    * FE02-FE09: ext4 fixes
- rediff patches:
    * DG00: drm-next
- disable in defconfigs:
    * LATENCYTOP - it bloats task_struct by effectively quadrupling
      the size of an otherwise lean task_struct

* Mon Jun  8 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.4-4mdv
- Release to Updates

* Mon Jun  1 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.4-3mdv
- resync drm patches with Fedora 2.6.29.4-167.fc11
    * DG01: drm: no gem on i8xx
    * DG03: drm: nouveau
    * DG10: drm: i915: apply a big hammer to 865 gem object
    * DG20: drm: copyback ioctl data to userspace regardless of retcode
    * DG21: drm: i915: fix tiling pitch
    * DG22: drm: intel: set domain on fault
- enable in defconfigs:
    * PCSPKR_PLATFORM, X86_CHECK_BIOS_CORRUPTION, EFI, IPV6_ROUTER_PREF,
    * IPV6_ROUTE_INFO, IPV6_OPTIMISTIC_DAD, IPV6_MROUTE, IPV6_PIMSM_V2,
    * IP_VS_IPV6, SCTP_HMAC_MD5, SERIAL_8250_RSA, CIFS_EXPERIMENTAL,
    * CIFS_DFS_UPCALL
- disable in defconfigs:
    * CONFIG_SYSFS_DEPRECATED_V2, KALLSYMS_EXTRA_PASS, SCTP_HMAC_NONE,
    * WIRELESS_OLD_REGULATORY
- set as module in defconfigs
    * IDE

* Sun May 31 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.4-2mdv
- stable queue patches:
    * AA01: xfrm: wrong hash value for temporary sa
    * AA02: tcp: fix-msg_peek-race-check
    * AA03: tcp: fix 2 iw selection
    * AA04: net: fix skb_seq_read returning wrong offset length for page
	    frag data
    * AA05: sch_teql: should not dereference skb after ndo_start_xmit
    * AA06: net: fix length computation in rt_check_expire
    * AA07: net: fix rtable leak in net ipv4 route.c
    * AA08: revert rose zero length frame filtering in af_rose.c
    * AA09: pktgen: do not access flows beyond its length
    * AA10: myr10ge: again fix lro_gen_skb alignment
    * AA11: vlan: macvlan: fix-null-pointer-dereferences-in-ethtool-handlers
    * AA12: mac8390: fix regression caused during net_device_ops conversion
    * AA13: bonding: fix alb mode locking regression
    * AA14: bonding: remove debug printk
    * AA15: r8169: avoid losing msi interrupts
    * AA16: sparc: fix bus type probing for esp and le devices
    * AA17: sparc64: fix smp_callin locking
    * AA18: mm: slub fix reclaim_state
    * AA19: fix: oops on close of hot unplugged ftdi serial converter
    * AA20: wimax: fix oops if netlink fails to add attribute
    * AA21: nfs: fix nfs v4 client handling of may_exec in nfs_permission
    * AA22: futex: setup writeable mapping for futex ops which modify user
	    space data
    * AA22: xen: blkfront allow xenbus state transition to closing closed
	    when not connected
    * AA23: tpm: get_event_name stack corruption
    * AA24: icom: fix rmmod crash
    * AA25: kvm: make paravirt tlb flush also reload the pae pdptrs
    * AA26: kvm: fix pdptr reloading on cr4 writes
    * AA27: cfg80211: fix race between core hint and drivers custom apply
- add drm patches from fc11.155
    * DG17: drm: intel include 965gme pci id
    * DG18: drm: intel i8xx cursors
    * DG19: drm: intel vmalloc
- add paches:
    * DN10: net: revert forcedeth power down phy when interface is down
    * FE05: ext4: really print warning once
    * FE06: ext4: prealloc fixes
    * FE07: ext4: fake delalloc bno
    * FE08: ext4: clear unwritten flag
    * FE09: ext4: fix i_cached_extent race

* Wed  May 20 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.4-1mdv
- update to 2.6.29.4 (CVE-2009-1184, CVE-2009-1337)
    * http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.29.4
    * http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.29.3
- add patches:
    * DG15: drm: intel tiling transition
    * DG16: drm: intel-next
    * DS04: fix usb gadget gmidi build with updated Alsa
- update patches:
    * DG00: drm: drm-next
    * DG02: drm: radeon modesetting
    * DG03: drm: nouveau
    * DM50: v4l-dvb snapshot 2009-05-16
    * DS01: Alsa 1.0.20+ 2009-05-16
    * DS02: Alsa 1.0.20+ buildfixes
    * DS10: selected Alsa unstable addons (maya44 &via vt1732)
- drop merged patches:
    * AA01-AA18: Stable Queue patches
    * DA01: ACPI: revert BIOS mangled PRT bugfix
    * DG14: drm: i915 allow tiled front buffers on 965
    * DM51: v4l-dvb snapshot buildfix
    * DS11: alsa sbxfi emu10k1 support (replaced in DS01 with ctxfi that
	    supports emu10k1, emu20k1 & emu20k2)
- update defconfigs

* Fri May  1 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.2-3mdv
- add patch DA01: ACPI: Revert conflicting workaround for BIOS with 
  mangled PRT entries (mdv bz #46222)

* Fri May  1 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.2-2mdv
- add patches from stable queue
    * AA13: b44: use kernel dma addresses for the kernel dma api
    * AA14: block: include empty disks in proc diskstats
    * AA15: crypto: ixp4xx: fix handling of chained sg buffers
    * AA16: exit_notify: kill the wrong capable check (CVE-2009-1337)
    * AA17: pci: fix incorrect mask of pm no_soft_reset bit
    * AA18: unreached code in selinux_ip_postroute_iptables_compat (CVE-2009-1184)

* Mon Apr 27 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.2-1mdv
- update to 2.6.29.2: CVE-2009-1192, CVE-2009-0795
    * http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.29.2
- drop patch AA00: 2.6.29.2-rc1
- add patches from stable queue:
    * AA02: mac80211: fix bug in getting rx status for frames 
	    pending in reorder buffer
    * AA03: b43: poison rx buffers
    * AA04: b43: refresh rx poison on buffer recycling
    * AA05: thinkpad-acpi: fix led blinking through timer trigger
    * AA06: mac80211: fix basic rate bitmap calculation
    * AA07: kvm-mmu: fix off by one calculating large page count
    * AA08: kvm-mmu: disable global page optimization
    * AA09: kvm: fix overlapping check for memory slot
    * AA10: kvm: x86 release time_page on vcpu destruction
    * AA11: usb: unusual device support for gold mp3 player energy
    * AA12: virtio-rng: remove false bug for spurious callbacks

* Fri Apr 24 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.1-5mdv
- add patches from stable queue:
    * AA00: 2.6.29.2-rc1
    * AA01: forcedeth: fix resume from hibernation regression
- rediff patches:
    * DG00: drm-next
    * DM50: v4l-dvb snapshot
    * DS01: alsa snapshot
- drop patches merged upstream:
    * AX01: pat fixes to allow GTT maps to work on intel
    * DM20: fix oops in md raid1

* Fri Apr 24 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.1-4mdv
- dm-raid45 target is finally back:
    * DM10: dm-raid45 20090424 for 2.6.29.1
    * DM13: add dm-raid4-5 modalias
- update defconfigs

* Sat Apr 18 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.1-3mdv
- add patches:
    * DG13: drm: ignore LVDS on intel graphics systems that lie about having it
    * DG14: drm: i915 allow tiled front buffers on 965+ (#50032)
    * DH20: hid: wacom bluetooth support
    * DI10: input: wacom intuos4 support (from main)
    * DM20: fix oops in md raid1
    * DU01: usb: add support for Qualcom usb modems
- update patches:
    * DG00: drm: drm-next
    * DG02: drm: radeon modesetting
    * DG03: drm: nouveau
    * DG06: drm: i915 resume force mode
    * KP01: TuxOnIce 3.0.1
    * NI01: net: netfilter ipset 2.4.9 (from main)
    * NI10: net: netfilter IFWLOG (from main)
    * NI11: net: netfilter IFWLOG mdv fixes (from main)
    * NI15: net: netfilter psd (from main)
    * NI16: net: netfilter psd mdv fixes (from main)
- drop patches:
    * DG11: drm: radeon: reorder busmaster vs. modeset (merged in DG02)
    * NI02-NI08: netfilter ipset buildfixes (not needed anymore)
    * NI12: netfilter IFWLOG buildfixes (not needed anymore)
    * NI17: netfilter psd buildfixes (not needed anymore)
- update defconfigs

* Sun Apr  5 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.1-2mdv
- rollback Alsa patches to earlier snapshot as current upstream
  is broken: (fixes #49385, #49536)
    * DS01: Alsa 1.0.19+ 2009-03-07
    * DS10: Alsa 1.0.19+ unstable addons 2009-03-07
- update patches:
    * FR01: Reiser4 for 2.6.29
    * KP01: TuxOnIce 3.0 Final
- drop patches:
    * FR02: Reiser4 buildfix

* Fri Apr  3 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29.1-1mdv
- update to 2.6.29.1
    * http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.29.1
- drop patches merged upstream:
    * DN10: Disable GRO on legacy netif_rx path
    * MC33: drbd bio_rw_sync fix (merged in drbd 8.3.1)
- add patches:
    * AX01: pat fixes to allow GTT maps to work on intel
    * DG11: drm: radeon: reorder busmaster vs. modeset
    * DG12: add "gem_enable" module option to i915
- update patches:
    * DG03: drm: nouveau update
    * MC30: drbd 8.3.1
- rediff patches:
    * DM50: v4l-dvb snapshot
    * MC31: drbd buildfixes
    
* Mon Mar 30 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-2mdv
- update patches:
    * DG00: drm-next update
    * DG02: radeon modesetting update
    * DG03: nouveau update
    * DI01: lirc update
    * KP01: TuxOnIce for 3.0-rc8 for 2.6.29
- add patches:
    * DH15: Asus atk0110 acpi hwmon support
- update configs
    
* Sat Mar 28 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-1mdv
- update to 2.6.29 final
- add patches:
    * FE02-FE04: ext4 delayed allocation fixes (from main kernel)
    * DM51: v4l-dvb staging go7007 buildfix
    * DN10: GRO: Disable GRO on legacy netif_rx path (from main kernel)
- update patches:
    * DG00: drm-next update
    * DG02: radeon modesetting update
    * DG03: nouveau update
    * DM50: v4l-dvb snapshot 20090327
    * DS01: Alsa 1.0.19+ snapshot 20090327
    * DS10: Alsa 1.0.19+ unstable addons snapshot 20090327
    * KP01: TuxOnIce 3.0-rc8 20090313
- drop patches merged upstream:
    * DM60: Hauppauge hdpvr (merged in v4l-dvb snapshot)
    * DN10: ipv6 module unload bug
    * FE01: ext4: extent-header check fix
- disable in defconfigs:
    * SYS_DEPRECATED(_V2), USB_DEVICE_CLASS, WIRELESS_OLD_REGULATORY
    * SND_SUPPORT_OLD_API
- update defconfigs

* Fri Mar 13 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc8.1mdv
- update to 2.6.29-rc8
- drop patches merged upstream:
    * FS10: squashfs page-aligned data fix
- update defconfigs

* Fri Mar 13 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc7.5.4mdv
- update to 2.6.29-rc7-git5
- update patches:
    * DG00: drm: drm-next update
    * DG02: drm: radeon modesetting support
    * DG03: drm: nouveau support
- add patches:
    * DG10: drm: fix flushing on i855, i865g
    * DS15: Alsa: hda_intel preallocate 4mb dmabuffer
    * DN10: ipv6: fix BUG when disabled ipv6 module is unloaded
    * FE01: ext4: extent-header check fix
    * FS10: squashfs: fix page-aligned data
    
* Wed Mar 11 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc7.3.3mdv
- update to 2.6.29-rc7-git3
- rediff patches:
    * DS01: Alsa 1.0.19+ snapshot
- drop patches merged upstream:
    * DA41: nVidia MCP89 support
    * DG07: drm setmaster deadlock fix
- drop patches fixed differently upstream:
    * DN02: bonding_ipv6 split:
	* Correct way to disable ipv6 support now is to add:
	  "options ipv6 disable=1" to /etc/modprobe.conf

* Sun Mar  8 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc7.2mdv
- update patches:
    * DG02: drm: radeon modesetting
    * DG03: drm: nouveau support
    * DI01: lirc support
    * DM50: v4l-dvb snapshot 20080307
    * DS01: Alsa 1.0.19+ snapshot 20080307
    * DS10: Alsa 1.0.19+ unstable addons snapshot 10080307
    * KP01: TuxOnIce 3.0-rc8 20090305
- add patches:
    * DA41: ahci: add support for nVidia MCP89
    * DG07: drm: fix setmaster deadlock
    * DG08: drm: add radeon PM support
- drop patches:
    * KP02: TuxOnIce buildfix (merged upstream)
- update defconfigs
    
* Wed Mar  4 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc7.1mdv
- update to 2.6.29-rc7

* Tue Mar  3 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc6.7.5mdv
- update to 2.6.29-rc6-git7
- drop patches:
    * AA02: fix build of drm i915 due to missing symbols (merged upstream)
- add patches:
    * DG00: drm-next (adds ati r600 support)
    * DM60: Hauppauge HD DVR support
- update patches:
    * DG02: drm: radeon modesetting
    * DG03: drm: nouveau
    * DI01: lirc
- rediff patches:
    * DS01: Alsa 1.0.19+ snapshot
- enable in defconfigs:
    * PM_DEBUG, IWLWIFI_DEBUG, IWL3945_DEBUG, DRM_NOUVEAU_KMS

* Sat Feb 28 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc6.5.4mdv
- update to 2.6.29-rc6-git5
- add patches:
    * AA02: fix build of drm i915 due to missing symbols
- update patches:
    * DM50: v4l-dvb snapshot 20090228
    * DN02: bonding_ipv6 split, v2 adds autoloading of the ipv6 part
    * DS01: Alsa 1.0.19+ snapshot 20090228
    * DS10: Alsa 1.0.19+ unstable snapshot 20090228
- rediff patches:
    * DG02: radeon modesetting
- drop patches:
    * DM51: v4l-dvb snapshot buildfix
- enable DMAR_DEFAULT_ON, SONYPI_COMPAT
- update defconfigs

* Wed Feb 25 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc6.1.3mdv
- update patches:
    * DG02: radeon modesetting support
- drop patches:
    * DG07: radeon modesetting pciid
    * DG08: radeon modesetting buildfix
- Enable DRM_RADEON_KMS, DRM_I915_KMS
    
* Tue Feb 24 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc6.1.2mdv
- update to 2.6.29-rc6-git1
- update defconfigs

* Mon Feb 23 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc6.1mdv
- update to 2.6.29-rc6:
    * http://www.eu.kernel.org/pub/linux/kernel/v2.6/testing/ChangeLog-2.6.29-rc6
- rediff patches:
    * DG02: radeon modesetting
    * DM50: v4l-dvb snapshot
    * DS01: Alsa snapshot
    * KP01: TuxOnIce
- add patches:
    * DG06: intel-gfx: fix kms S3 resume
    * DG07: drm: fix pciids when using radeon modesetting
    * DG08: fix radeon modesetting build
    * KP02: tuxonice fix for bio_rw_sync change
    * MC33: drbd: adapt for bio_rw_sync change (Herton, main kernel)
- drop patches:
    * DG04: intel-next (merged ustream)
    * DP01: Intel Mobile 4 write buffer flush capacity fix (merged upstream)
- enable full PREEMPT on -desktop(586) kernels to see what breaks
- add drivers/acpi/acpica header files to -devel rpms, needed by fglrx
- update defconfigs
    
* Sat Feb 21 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc5.4mdv
- - update patches:
    * DM50: v4l-dvb snapshot 2009-02-18
    * DM51: v4l-dvb snapshot buildfix
    * DS01: Alsa 1.0.19+ snapshot 2009-02-18
    * DS02: Alsa snapshot buildfix
    * DS10: Alsa unstable addons 2009-02-18
- add patches:
    * DN02: split bonding for ipv6 to separate module, to allow disabling
	    of ipv6 at runtime without breaking bonding for ipv4
- update defconfigs
    
* Wed Feb 18 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc5.3mdv
- add patches to fix netfilter crash (thanks Herton)
    * NI12: ipt_IFWLOG buildfix
    * NI17: ipt_psd buildfix
- add patch DG02: drm: modesetting for radeon
- add patch DG03: drm: nouveau driver
- add patch DG04: drm: intel-next
-update defconfigs

* Sun Feb 15 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc5.2mdv
- enable TASKSTATS, TASK_DELAY_ACCT, TASK_XACCT, TASK_IO_ACCOUNTING (#47818)
- update and enable patch KP01: TuxOnIce 3.0-rc8 2009-02-14
- add patch DG01: disable GEM on i8xx gpu
- add patch DI01: lirc support
- add patch DP01: Force write-buffer flush capability on Intel Mobile 4 
  chipset as it needs it to work properly
- update defconfigs

* Sat Feb 14 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc5.1mdv
- update to 2.6.29-rc5
- add patches NI07, NI08: ipset apifixes for 2.6.29 (Herton, from main kernel)
- update defconfigs

* Thu Feb 12 2009 Thomas Backlund <tmb@mandriva.org> 2.6.29-0.rc4.1.1mdv
- update to 2.6.29-rc4-git1
- drop patches merged upstream:
    * AA01: md: device limit fix
    * AX01, AX02: Amd 0x11 nb support    
    * AX05: Amd Fam10h APIC workaround
    * AX10: more pcore fsbs for cpufreq
    * AX15: Intel Core i7 cache descriptors
    * DA01-DA09: ACPICA 20080926 uppdate    
    * DA40: Promise PDC42819 AHCI support
    * DA45: Intel Ibex Peak device ids
    * DC01: Intel G41 agp support
    * DN02: bonding ethtool support
    * DN10: r8169 update
    * DN15-DN16: Intel e1000e 82567xx support
    * DN20: atl2 support
    * DN30: Jmicron gigabit ethernet
    * DN40: amd8111e bugfix
    * DN41: Atheros AR8021 support
    * DN42: SM LAN921-5-7-8 support
    * DN43: p54usb device is updates
    * FS02: security_inode_permission symbol export
    * FS10-FS15: ext4 updates
    * MB20: squashfs 3.4 (squashfs 4 is now upstream)
    * MC33-MC35: drbd buildfixes
    * MC60: 3rdparty at76_usb (is now in upstream staging tree)
    * MD10-MD13: 3rdparty prism25 (is now in upstream staging tree)
- update pathes:
    * CE02: acpi-dsdt-initrd v0.9c-2.6.28
    * DM10: dm-raid45 for 2.6.29-rc
    * DM50: v4l-dvb snapshot 2009-02-07
    * DS01: Alsa 1.0.19+ snapshot 2009-02-07
    * FR01: reiser4 support
    * FS01: unionfs 2.5.1
    * MB02: 3rdparty merge
    * MC30-MC32: drbd 8.3.0
    * NI15: ipt_psd
- disable patches:
    * DB32: sis5513-965 ide fix
    * DH01: multilaser usbhid fix
    * DM10, DM13: dm-raid45 (broken build)
    * KP01: TuxOnIce 3.0-rc8 (broken build)
- add patches:
    * AA01: add missing memcontrol include to mm_config.h
    * FR02: reiser4 buildfix
    * MC42: fsc_btns buildfix
- fix -devel and -source filelists and content
- enable staging tree
- make HID core modular
- drop sparc64 support
- update defconfigs
                                   
* Sun Feb  8 2009 Thomas Backlund <tmb@mandriva.org> 2.6.27.15-2mdv
- add patch AX05: fix boot with AMD Fam10h CPUs on systems with broken
  or missing MP table
- add patch AX15: add cache descriptors for Intel Core i7
- update patch DM50: v4l-dvb snapshot 2009-02-07
    * bugfixes, updates
    * adds bttv support for IVCE-8784
    * adds cx23885 support for TurboSight TBS 6920, TeVii S470,
      DVBWorld DVB-S2 2005
    * adds en28xx support for Gadmei TVR200
    * adds gspca support for Creative Live! Cam Notebook Ultra (VC0130),
      Aiptek PenCam VGA+, Genius iLook 111
    * add zr364xx support for Aiptek DV T300
- update patch DM51: v4l-dvb snapshot buildfixes
- update patch DS01: Alsa 1.0.19+ snapshot 2009-02-07
    * bugfixes, updates
    * adds support for Turtle Beach MultiSound Classic, Tahiti, Monterey,
      and Pinnacle/Fiji soudcards
    * adds support for Tyan Thunder n6650W (S2915-E)
- update patch DS02: alsa snapshot buildfixes
- drop patch DS04: Sony Vaio VGN FZ18M quirk (fixed differently upstream)
- update patch DS10: Alsa unstable addons snapshot 2009-02-07
- add patch DS11: Alsa SB X-Fi support (broken out from unstable snapshot)
- redo patch KP01: TuxOnIce 3.0-rc8 for 2.6.27.15 from a clean git clone
- drop patch KP02: TuxOnIce buildfix (not needed anymore)
- update create_configs script for TuxOnIce update
- update defconfigs

* Sat Feb  7 2009 Thomas Backlund <tmb@mandriva.org> 2.6.27.15-1mdv
- update to 2.6.27.15:
    * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.27.15
- update to 2.6.27.14:
    * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.27.14
- add patches from stable queue:
    * AA01: md: ensure an md array never has too many devices
- rediff patch DA01: acpica 2008-09-26 update
- rediff patch DS01: Alsa 1.0.19 final
- update patch KP01: TuxOnIce 3.0-rc8 for 2.6.27.15
- add patch KP02: revert tuxonice_userui code not in 2.6.27

* Sun Feb  1 2009 Thomas Backlund <tmb@mandriva.org> 2.6.27.13-2mdv
- bump release to get past kernels in testing tree

* Sun Jan 25 2009 Thomas Backlund <tmb@mandriva.org> 2.6.27.13-1mdv
- update to kernel.org 2.6.27.13:
  * http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.27.13
- rediff patch DS01: Alsa 1.0.19
- drop patches DU01, DU02: usb-storage support for Nokia 5610 & 7610,
  not needed anymore as it's fixed on vendor level in 2.6.27.13
  (cf usb-storage: set CAPACITY_HEURISTICS flag for bad	vendors)
- drop patch FS10: ext4 patchset 2.6.27-ext4-2
- add new patch FS10: ext4 stable backports queue
- add patch FS11: ext4 Add blocks added during resize to bitmap
- add patch FS12: ext4 Use EXT4_GROUP_INFO_NEED_INIT_BIT during resize
- add patch FS13: ext4 Use an rbtree for tracking blocks freed during
		  transaction
- add patch FS14: ext4 Dont use blocks freed but not yet committed 
		  in buddy cache init
- add patch FS15: ext4 Use new buffer_head flag to check uninit group 
		  bitmaps initialization
- update patch KP01: TuxOnIce 3.0-rc8 for 2.6.27.13
- update defconfigs

* Mon Jan 19 2009 Thomas Backlund <tmb@mandriva.org> 2.6.27.12-2mdv
- rediff patch DM50: cleaner v4l-dvb snaphot 2009-01-18
- update/rediff patch DM51: v4l-dvb buildfix zoran_card build under ix86
- update patch DS01: Alsa 1.0.19 Final
- rediff patch DS02: Alsa buildfixes
- rediff patch DS10: Alsa unstable addons
- update patch FS01: unionfs 2.5.1

* Mon Jan 19 2009 Thomas Backlund <tmb@mandriva.org> 2.6.27.12-1mdv
- update to 2.6.27.12: (CVE-2009-0029)
  * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.27.12
- update to 2.6.27.11:
  * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.27.11
- drop patch AA01-AA06: stable-queue patches (merged upstream)
- update patch DM10: dm-raid45 2008-10-27
- drop patches DM11, DM12: dm-raid45 buildfixes (merged upstream)
- update patch DM13: dm-raid4-5 modalias
- update patch DM50: v4l-dvb snapshot 2009-01-18
- update patch DM51: v4l-dvb snapshot buildfix
- update patch DS01: Alsa 1.0.18+ snapshot 2009-01-18
- update patch DS02: Alsa dnapshot buildfix
- rediff patch DS10: Alsa unstable addons 2009-01-18
- drop old patches FR01-FR14: reiser4 patches from old akpm patchset
- add new patch FR01: reiser4 for 2.6.27 updated 2009-01-15
- update patch KP01: TuxOnIce 3.0-rc8
- update create_configs for the new TuxOnIce
- update defconfigs

* Sun Dec 28 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27.10-2mdv
- add pathes from Stable queue:
  * AA01: usb-gadget: fix rndis working at high speed
  * AA02: usb-storage: update unusual_devs entry for nokia 5310
  * AA03: usb-storage: add unusual_devs entry for nokia 3109c
  * AA04: usb-storage: add unusual_devs entry for nokiav3500c
  * AA05: powerpc: fix corruption error in rh_alloc_fixed
  * AA06: iwlagn: downgrade bug_on in interrupt
- Add patches from main kernel:
  * AX01, AX02: add detection of AMD family 0x11 northbridges
  * AX10: add more pcore fsbs to cpufreq
  * DH10: add hwmon coretemp support for Intel Atom
  * DU01, DU02: add usb-storage support for Nokia 5610 & 7610

* Sat Dec 20 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27.10-1mdv
- update to 2.6.27.10
  * http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.27.10
- update to 2.6.27.9 (CVE-2008-5079)
  * http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.27.9
- update to 2.6.27.8 (CVE-2008-5300)
  * http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.27.8
- update to 2.6.27.7 (CVE-2008-5033)
  * http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.27.7
- update patch DM50: v4l-dvb snapshot 2008-12-20
  * adds support for: 
    Phytec VD-012, Compro VideoMate E650F, Sattrade ST4200 DVB-S/S2,
    TBS 8910 DVB-S, Prof 6200 DVB-S, Pinnacle PCTV HD Mini,
    Hauppauge WinTV HVR 850, Kworld Plus TV Analog Lite PCI
  * adds gspca support for: 
    Hercules Blog Webcam, Hercules Dualpix HD Weblog, Hercules Classic Silver,
    Genius Eye 312, Microdia Audio, Microdia Sonix PC Camera, 
    Sony HD Eye for PS3 (SLEH 00201), Trust WB-1300N, HP 2.0 Megapixel rz406aa
- drop patch AA01: fix broken ownership of proc sys files (merged upstream)
- rediff patch DA01: acpica 20080926 update
- drop patch DI01: ALPS support for Latitude E6500 (merged upstream)
- rediff patch FS10: ext4 update
- update patch DS01: Alsa 1.0.18+ snapshot 2008-12-20
  * adds support for:
    - Olpc XO-1 additional sound features
    - low volume boost on Audigy
  * HD Audio and HDMI updates including:
    - add quirk for Medion MD96630
    - fix Samsung R60, X11, X60 quirks
    - add quirks for HP 6730b, 6730s, EliteBook 8530p, dv5, dv7
    - adds support for nVidia MCP67 HDMI, Asus P5Q-EM HDMI
    - adds support for Acer Aspire 4930G, Fujitsu Amilio XA3530
    - adds support for MSI 7260, HT Omega Claro Halo
    - add quirks for Dell Studio 1537, Studio17
  * Adds support for a lot of Digigram based cards:
    - VX882E, PCX882E, VX881E, PCX881E, VX1222HR, VX1221HR, VX1222E, PCX1222E,
      VX1221E, PCX1221E, VX222HR, VX222E, PCX22HR, PCX22E, VX222HRMIC,
      VX222E_MIC, PCX924HR, PCX924E, PCX924HRMIC, PCX924E_MIC
- update patch DS02: Alsa 1.0.18+ buildfixes 2008-12-20
- update patch DS10: Alsa unstable adddons 2008-12-20
- update defconfigs

* Wed Nov 19 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27.6-2mdv
- add patch AA01: fix broken ownership of proc sys files

* Sun Nov 16 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27.6-1mdv
- update to 2.6.27.6 (CVE-2008-5025)
- drop patch DM01: raid10 recovery bugfix (merged upstream)
- rediff patch DA01: acpica update
- rediff patch DN10: r8169 updates
- rediff patch DS01: Alsa update
- update defconfigs

* Sun Nov  9 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27.5-3mdv
- rename acpi patches to prepare for acpi fixes:
  * change patch DA30 prefix to DA01 (acpica update)
  * change patch DA31 prefix to DA02 (acpica buildfix)
- add acpi patches:
  * DA03: i7300_idle: Disable ioat channel only on platforms where idle can load
  * DA04: i7300_idle: Cleanups
  * DA05: i7300_idle: Fix compile warning about I7300_IDLE_IOAT_CHANNEL not defined
  * DA06: suspend: build fix for ACPI_SLEEP=n & XEN_SAVE_RESTORE=y
  * DA07: fix Oops in pci-acpi
  * DA08: toshiba_acpi: depends on INPUT
  * DA09: make dock driver not a module as it needs to be loaded before libata
- add patch DA40: ahci: add support for Promise PDC42819 in sata mode
- add patch DN02: bonding: add more ethtool support
- add patch DN40: amd8111e: fix dma_free_coherent context bug
- add patch DN41: sis190: add support for Atheros AR8021 PHY
- add patch DN42: smc911x: add support for LAN921-5-7-8 chips
- add patch DN43: p54usb: add support for SMC 2862W-G version 2

* Sat Nov  8 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27.5-2mdv
- update patch DA30: ACPICA 2008-09-26
- disable old acpi patches to see if they are needed anymore:
  * DA15: acpi-add-proc-event-regs
  * DA20: acpi-asus-laptop-input
  * DA21: acpi-asus-eee
  * DA22: acpi-asus-disable-autoload-on-asus-laptops
  * DA25: acpi-CELVO-M360S-disable_acpi_irq
  * DA26: acpi-processor-M720SR-limit-to-C2
- update defconfigs

* Fri Nov  7 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27.5-1mdv
- update to 2.6.27.5
- rediff patch DA30: acpica update
- drop patch DA35: sata_nv hardreset fix (merged upstream)
- add patch DA45: ata support for Intel Ibex Peak (PCH)
- rediff patch DC01: Intel G41 AGP support
- add patch DM01: fix raid10 recovery bug
- update patch DM50: v4l-dvb snapshot 2008-11-07
  * adds STB0899, STB6100, Philips TDA8261, LG LGDT3304, 
    Sharp S921 dvb support
  * adds Finepix, SunPlus usb webcam support
- add patch DM51: revert dvb changes not supported by 2.6.27 kernel
- add patch DN15: Intel 82567LM-4 gigabit lan support
- add patch DN16: Intel (ich10) 82567LF-3 and LM-3 gigabit lan support
- update patch DS01: Alsa 1.0.18+ snapshot 2008-11-07
  * adds hrtimer backend support
  * adds Intel hdmi audio support
  * adds support for some more laptops
- add patch DS02: revert Alsa changes not supported by 2.6.27 kernel
- add patch DS10: Selected updates from Alsa -unstable tree
  * adds support for Creative X-Fi CA0110-IBG codec
  * adds support for Creative X-Fi Emu20k1 chip
  * adds support for VIA VT1732 (Envy24-II)
  * adds support for several Gateway systems
- update defconfigs

* Sun Oct 26 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27.4-2mdv
- update patch DN10: updates r8169 to 2.6.28-rc2 level
  * fixes possible "brick" bug
- drop patch DN11: r8169 NULL pointer fix (merged upstream)

* Sun Oct 26 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27.4-1mdv
- update to 2.6.27.4 final
- drop patch AA01: 2.6.27.4-rc3 (merged upstream)

* Sat Oct 25 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27.3-1mdv
- update to 2.6.27.3 final
- update patch AA01: 2.6.27.4-rc3
- rediff patch DA30: acpica 20080729
- update patch FS10: ext4 update to 2.6.27-ext4-2
- enable EXT4DEV_COMPAT so userspace expecting to mount ext4dev
  instead of ext4 wont break
- update defconfigs

* Sun Oct 19 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27.2-1mdv
- update to 2.6.27.2
- add patch AA01: 2.6.27.3-rc1
- add patch DN11: fix NULL pointer dereference on r8169 load
  (Reported by Charles, fix pointed out by Andrey)
- drop patch FS15: XFS barrier fail detection fix, merged upstream

* Thu Oct 16 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27.1-1mdv
- update to 2.6.27.1
  * disables CONFIG_DYNAMIC_FTRACE due to possible memory corruption
    on module unload (this  is the reason e1000e cards broke)
      
* Sat Oct 11 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-2mdv
- drop patches DA10-DA12: tc1100-wmi, all needed support is 
  already in 2.6.27
- drop old patch DA30: acpi ec 2.1 (merged in updated ACPICA)
- add patch DA30: ACPI and ACPICA 2008-07-29 update
  * improvements for docking, bay and hotplug
  * better errror messages, support more laptops
  * better rfkill support
- add patch DA31: export symbol acpi_os_hotplug_execute
- add patch DI01: Alps touchpad support for Dell Latitude E6500 (#44701)
- update patches DM10-DM12: rename dm-raid4-5 to dm-raid45 as
  that's what the kernel expects to find.
- add patch DM13: add dm-raid4-5 modalias to dm-raid45 to not break updates
- update defconfigs

* Sat Oct 11 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-1mdv
- update to 2.6.27 final
- add patch DA35: sata_nv hardreset fix
- update patch DM50: v4l-dvb snapshot 2008-10-10
- drop patch DM51: saa7134-alsa fix, fixed in DS01
- update patch DN10: even more r8169 fixes
  * from: http://userweb.kernel.org/~romieu/r8169/2.6.27-rc9
- update patch DS01: Alsa 1.0.18rc3.1 snapshot 2008-10-10
- add patch FS10: ext4 updates to 2.6.27-rc9-ext4-1
- add patch FS15: fix barrier fail detection in XFS
- update patch KP01: TuxOnIce 3.0-rc7 for 2.6.27
- update patch MC34: rename drbd WARN macro to DRBD_WARN
- add patch MC35: drbd: fix cn_idx_drbd definition
- update defconfigs

* Mon Oct  6 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc8.8.1mdv
- update to 2.6.27-rc8-git8
- update patch DM50: v4l-dvb snapshot 2008-10-06
- add patch DM51: convert saa7134-alsa to snd_BUG_ON
- add patch DN10: support more r8169 network cards
  * from: http://userweb.kernel.org/~romieu/r8169/2.6.27-rc6/
- drop patch DS00: alsa revert 
- update patch DS01: Alsa 1.0.18rc3.1 snapshot 2008-10-06
- update defconfigs

* Thu Oct  2 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc8.3.1mdv
- update to 2.6.27-rc8-git3
  * contains workaround for e1000e hw breaking bug
- drop patches MC50-MC54: acx wireless, due to legal reasons
- drop patch DA55: sata_nv regression fix, merged upstream
- add patch DS00: revert upstream alsa fixes already in Alsa 1.0.18rc3
- add patches MC33, MC34: drbd fixes (from main)
- update defconfigs

* Sun Sep 28 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc7.5.2mdv
- update to 2.6.27-rc7-git5
- add patch DA30: acpi ec v2.1, adds fast transaction (from main)
- add patch DA55: fix sata_nv regression (#44287, from main)
- add patch DC01: add support for intel G41 chipset (from main)
- update patch DM50: v4l-dvb snapshot 2008-09-28
- add patch DN30: add support for JMicron Gigabit ethernet (from main)
- update defconfigs

* Fri Sep 26 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc7.4.1mdv
- update to 2.6.27-rc7-git4
- add patch FS02: export security_inode_permission, as unionfs needs it.

* Sun Sep 21 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc6.6.1mdv
- update to 2.6.27-rc6-git6
- update patch FS01: unionfs v2.5

* Sat Sep 13 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc6.2.1mdv
- update to 2.6.27-rc6-git2
- update patches FR01-FR15: Reiser4 from 2.6.27-rc5-mm1
- update patch DS01: Alsa 1.0.18rc3 (from main)
- update patch DM50: v4l-dvb snapshot 2008-09-13
- add patch NI06: fix netfilter ipset build on 2.6.27 (from main)
- change versioning to show git snapshot like kernel-linus
- redo defconfigs based on main kernel defconfigs with the following changes:
  * disable TASKSTATS, NAMESPACES, SLUB_DEBUG, BLK_DEV_IO_TRACE, IP_VS_DEBUG
  * disable BLK_DEV_UB, SCSI_SAS_LIBSAS_DEBUG, AIC94XX_DEBUG, B43_DEBUG
  * disable B43LEGACY_DEBUG, HID_DEBUG, REISERFS_PROC_INFO
  * disable OCFS2_DEBUG_MASKLOG, CIFS_STATS2, KEYS_DEBUG_PROC_KEYS
  * change NR_CPUS to 16
  * enable MD_FAULTY, DM_DELAY, FIREWIRE, FIREWIRE_OHCI, FIREWIRE_SBP2
  * enable FIREWIRE_OHCI_REMOTE_DMA, TULIP_MMIO, TULIP_NAPI, 
  * enable TULIP_NAPI_HW_MITIGATION, SUNDANCE_MMIO, VIA_RHINE_MMIO
  * enable HIPPI, ROADRUNNER, VIDEO_VIVI, DVB_USB_DIBUSB_MB_FAULTY
  * enable AUTOFS_FS, KARMA_PARTITION, DETECT_SOFTLOCKUP, EARLY_PRINTK
  * enable 4KSTACKS, CRYPTO_DEV_HIFN_795X_RNG

* Sat Aug 30 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc5.1mdv
- update to 2.6.27-rc5
- require kernel-firmware from main
- remove /lib/firmware from the rpms
- parallelize xargs invocations on smp machines
- add patch DM12: fix dm-raid45 build with 2.6.27
- update patch DM50: dvl-dvb snapshot 2008-08-29
- drop patch DN05: support wm6 devices as modems (merged upstream)
- update patch DN20: atl2 support for 2.6.27 series (from main)
- update patch DS01: Alsa snapshot 2008-08-27 (from main)
- drop old patches FR01-FR17: reiser4 support
- add new FR01-FR12: Reiser4 support from 2.6.27-rc1-mm1
- add patch FR13: Reiser4 buildfix for 2.6.27-rc5
- update patch FS01: unionfs 2.4.0 for 2.6.27-rcX
- drop patch FS10: ext4 snapshot (merged upstream)
- update patch KP01: TuxOnIce 3.0-rc7
- drop patch KS01: disabling of SCHED_HRTICK, as it's now fixed upstream
- update patch MB02: 3rdparty merge (from main)
- add patch MB13: ndiswrapper buildfix for 2.6.27 (from main)
- update patch MB20: squashfs 3.4 (from main)
- drop patch MB21: squashfs buildfix (not needed anymore)
- add patch MC54: acx buildfix for 2.6.27 (from main)
- drop old patches MC60-MC61: old Atmel wireless support
- add new patch MC60: Atmel at76 wireless support (from main)
- update patches MD10-MD13: Prism2 0.2.9 r1859 (from main)
- update defconfigs

* Wed Aug 20 2008 Thomas Backlund <tmb@mandriva.org> 2.6.26.3-1mdv
- update to 2.6.26.3:
  * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.26.3
- update patch DM50: remove tea575x-tuner changes as a more complete
  one is in Alsa-1.0.18-rc1
- update patch DS01: Alsa 1.0.18rc1
- drop patch DS03: Nec Versa S9100 support (merged upstream)
- update patch FS10: ext4 support: 2.6.26-ext4-7
- make TuxOnIce builtin and default on -laptop flavour
- add patch KS01: really disable CONFIG_SCHED_HRTICK as it's known to 
  cause boot problems with at least Intel GMA cards, as noted on LKML 
  and kernel.org BugZilla #10892
- update defconfigs

* Fri Aug  8 2008 Thomas Backlund <tmb@mandriva.org> 2.6.26.2-1mdv
- update to 2.6.26.2:
  * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.26.2
- drop patches AA01-AA18: stable queue fixes, merged upstream
- add patch DN06: John Carrs 'dirty patch' to usb rndis_host,
  fixes support of several WM devices
- update patch DS01: Alsa 1.0.17+ 2008-07-27
- drop patches DS02-DS16: alsa fixes, merged in DS01
- add patch DS02: alsa: bluetooth SCO support
- add patch DS03: alsa: support NEC Versa S9100
- add patch DS04: alsa: support Sony Vaio VGN FZ18M
- add patch DS05: alsa: support Toshiba Pro A200/A210
- drop patch DV01: bootsplash support, as we now use splashy
- update defconfigs

* Mon Aug  4 2008 Thomas Backlund <tmb@mandriva.org> 2.6.26.1-2mdv
- update patch FS10: ext4 update to 2.6.26-ext4-5
- fix missing bounds.h in -devel rpms
- dont prepare -source tree at all
- keep disable-prepare-scripts as a separate patch like main
- disable removal of asm-offsets.h and bounds.h in -devel rpms (Herton)

* Sat Aug  2 2008 Thomas Backlund <tmb@mandriva.org> 2.6.26.1-1mdv
- update to 2.6.26.1:
  * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.26.1
- drop patch AA01: 2.6.26.1-rc1 (merged upstream)
- add patches from stable queue:
    * AA01: ftrace: remove unneeded documentation
    * AA02: romfs: readpage dont report errors for pages beyond i_size
    * AA03: netfilter: nf nat_sip c is optional for session
    * AA04: scsi: bsg fix bsg_mutex hang with device removal
    * AA05: x86: idle process add checking for null early param
    * AA06: x86: io delay add checking for null early param
    * AA07: md: close race in md_probe
    * AA08: kprobe: smoke test lockdep warning
    * AA09: netfilter: xt_time fix time s time_mt s use of do_div
    * AA10: md: linear correct disk numbering error check
    * AA11: scsi: ch fix ch_remove oops
    * AA12: nfs: ensure we zap only the access and acl caches when setting new acls
    * AA13: jbd: fix race between free buffer and commit transaction
    * AA14: input: i8042 add intel d845pesv to nopnp list
    * AA15: input: i8042 add gericom bellagio to nomux blacklist
    * AA16: input: i8042 add acer aspire 1360 to nomux blacklist
    * AA17: bluetooth: signal userspace for hidp and bnep socket errors
    * AA18: ptrace: add compat handler for ptrace_getsiginfo
- update patch FS01: unionfs 2.4
. drop patch FS02: unionfs prototype fix (not needed anymore)
- add patch FS10: 2.6.26-ext4-4 patchset, makes ext4 ready for wider
  testing according to upstream

* Fri Aug  1 2008 Thomas Backlund <tmb@mandriva.org> 2.6.26-4mdv
- drop patches AA01-AA19: stable queue fixes (included in 2.6.26.1-rc1)
- add new AA01: 2.6.26.1-rc1
- add patch DM10: dm-raid4-5 support
- add patch DM11: dm-raid4-5 buildfixes for 2.6.26 series kernels
- rediff patch DM50: v4l-dvb snapshot
- rediff patch DS01: alsa 1.0.17
- update defconfigs

* Sun Jul 27 2008 Thomas Backlund <tmb@mandriva.org> 2.6.26-3mdv
- change desktop586 kernels back to 1GB RAM until someone actually
  needs 4GB on i586
- add patches from stable queue:
    * AA01: pxamci: trivial fix of dma alignment register bit clearing
    * AA02: udplite: protection against coverage value wrap-around
    * AA03: ipv6: use timer pending
    * AA04: ipv6: __kernel__ ifdef struct ipv6 devconf
    * AA05: hdlcdrv: fix crc calculation
    * AA06: quota: fix possible infinite loop in quota code
    * AA07: isofs: fix minor filesystem corruption
    * AA08: kvm: vmx fix a wrong usage of vmcs_config
    * AA09: kvm: svm fix suspend resume support
    * AA10: kvm: mmu_shrink kvm_mmu_zap_page requires slots_lock to be held
    * AA11: kvm: vmx add ept_sync_context in flush_tlb
    * AA12: kvm: x86 emulator fix hlt instruction
    * AA13: kvm: mmu nuke shadowed pgtable pages and ptes on memslot destruction
    * AA14: kvm: mmu fix potential race setting upper shadow ptes on nonpae hosts
    * AA15: ptrace: fix ptrace_getfpxregs error
    * AA16: rcu: fix rcu_try_flip_waitack_needed to prevent grace period stall
    * AA17: signal: fix typos from signal_32-64.h merge
    * AA18: x86: reboot quirks add dell precision workstation t5400
    * AA19: usb: fix usb serial pm counter decrement for disconnected interfaces
- update patch CE02: acpi dsdt initrd v0.9a
- update patch DM50: v4l-dvb snapshot 2008-07-27
- drop patch DM51: v4l-dvb buildfix (merged upstream)
- drop patch FS20: broken isofs rockridge fix (it's now -stable AA07)
- update patch KP01: TuxOnIce 3.0-rc7 2008-07-27
- redo kernel-tmb.patchlist
- update defconfigs

* Thu Jul 24 2008 Thomas Backlund <tmb@mandriva.org> 2.6.26-2mdv
- add patch DN05: rndis_host: support WM6 devices as modems
- add fixes and updates from ALSA:
  * DS02: add TriTech 28023 AC97 codec ID and Wolfson 97
  * DS03: Au1xpsc psc not disabled when TX is idle
  * DS04: re-order AC97 codec ID-table
  * DS05: hda Align BDL position adjustment parameter
  * DS06: ens1370 SRC stands for Sample Rate Converter
  * DS07: sound alsa ens1370 communicate PCI device to AC97
  * DS08: ASoC Refactor DAPM event handler
  * DS09: ASoC Factor PGA DAPM handling into main
  * DS10: hda Added support for Asus V1Sn
  * DS11: opti93x Fix NULL dereference
  * DS12: opti9xx no isapnp param for CONFIG_PNP
  * DS13: hda Add support of ASUS Eeepc P90
  * DS14: hda digital pc beep support hd audio codecs
  * DS15: soc wm9712 mono mixer
  * DS16: hda Add automatic model setting for Acer Aspire 5920G

* Tue Jul 22 2008 Thomas Backlund <tmb@mandriva.org> 2.6.26-1mdv
- update to 2.6.26
- drop patches AA01-AA29: -stable-queue fixes (merged upstream)
- disable patch DA04: acpi double proc entries fix (broken)
- drop patch DA30: acpi video ignore unsupported devices (merged upstream)
- disable patches DM10, DM11: dm-raid45 support (broken)
- update patches DM50, DM51: v4l-dvb snapshot as of 2008-07-22
  * new drivers:
    - Gspca, Sensoray 2255, DvbWorld 2102 DVB-S, Anysee DVB-T/C
    - Siano SMS1XXX, Micronas DRX3975D/DRX3977D
- update patch DN20: atl2 nic 2.0.4 (from main)
- drop patch DN21: atl2 nic buildfix (fixed upstream)
- rediff patch DS01: Alsa 1.0.17
- drop patch DS02: alsa compat fix (not needed anymore)
- drop patch FF01: fat: allow utime (merged upstream)
- add patch FS02: unionfs buildfix for 2.6.26
- drop patches FS10-FS12: UDF 2.50 read support (merged upstream)
- rediff patch KP01:TuxOnIce 3.0-rc7
- drop old/obsoleted patches from 3rdparty tree:
  * MB50-MB52: qc-usb v0.6.6 (replaced by intree drivers)
  * MB60-MB65: ipw3945 v1.2.2 (replaced by the intree iwl* drivers)
  * MB70-MB72: rt2400 v1.2.2-cvs (replaced by the intree rt2* drivers)
  * MB80-MB82: rt2500 v1.1.0-cvs (replaced by the intree rt2* drivers)
  * MB90-MB92: rt2570 v1.0.0-cvs (replaced by the intree rt2* drivers)
  * MC00-MC03: rt61 v1.1.0-cvs (replaced by the intree rt5* drivers)
  * MC10-MC13: rt73 v1.0.3.6-cvs (replaced by the intree rt7* drivers)
  * MD00-MD01: uvc r205 (merged upstream)
- update patch MC30, MC31: drbd v8.2.6
- update patch MC40: fsc_btns 1.40
- add patch MD11: prism25 buildfix for 2.6.26
- drop patch NW01: dummy ieee80211_regdom parameter (not needed anymore)
- update defconfigs
- fix sigframe.h in -devel rpms
- add /firmware to -devel and -source rpms
- add kernel/bounds.c to -devel rpms
- fix disable-mrpoper patch to apply cleanly 
- drop spec fix for #29744, #29074 (not needed anymore)

* Sun Jul 20 2008 Thomas Backlund <tmb@mandriva.org> 2.6.25.11-2mdv
- add patches AA01-AA29: Fixes from -stable queue:
  * b43legacy: do not return tx_busy from op_tx
  * b43: do not return tx_busy from op_tx
  * b43: fix possible mmio access while device is down
  * mac80211: detect driver tx bugs
  * block: fix the starving writes bug in the anticipatory io scheduler
  * md: fix error paths if md_probe fails
  * md: dont acknowlege that stripe expand is complete until it really is
  * md: ensure interrupted recovery completed properly
  * block: properly notify block layer of sync writes
  * ohci: fix problem if sm501 and another platform driver is selected
  * usb-ehci: fix timer regression
  * usb-ohci: record data toggle after unlink
  * usb: fix interrupt disabling for hcds with shared interrupt handlers
  * hdaps: add support for various newer lenovo thinkpads
  * b43legacy: fix possible null pointer dereference in dma code
  * netdrvr: 3c59x remove irqs_disabled warning from local_bh_enable
  * scsi: esp fix oops in esp_reset_cleanup
  * scsi: esp tidy up target reference counting
  * scsi: ses fix timeout
  * mm: switch node meminfo active inactive pages to kbytes
  * reiserfs: discard prealloc in reiserfs_delete_inode
  * cciss: read config to obtain max outstanding commands per controller
  * serial: fix serial_match_port for dynamic major tty device numbers
  * can: add sanity checks
  * sisusbvga: fix oops on disconnect
  * md: ensure all blocks are uptodate or locked when syncing
  * textsearch: fix boyer moore text search bug
  * netfilter: nf_conntrack_tcp fixing to check the lower bound of valid ack
  * zd1211rw: add id for airties wus 201
- update patch DS01: Alsa 1.0.17 Final
- update and enable patch FS10: UDF 2.50 support
- add patch FS11: disable UDF_DEBUG
- add patch FS12: fix regression in udf anchor block detection
- add patch FS20: enable reading of cds with broken rockridge data
- disable -rt patchset and -realtime on 2.6.25 series, it has
  way too many problems for now for a stable *tmb* series
- add patch NW01: add dummy ieee80211_regdom parameter to cfg80211
  so it will work on systems that assume a 2.6.26+ series kernel
- switch back to SLUB from SLAB
- enable Reiser4 fs again
- disable USB_KBD and USB_MOUSE, only needed on embedded systems
- change -laptop kernel config options to save more power:
  * HZ_300 -> HZ_250 (lowest that works with audio)
- change -server kernel config options
  * HZ_100 -> HZ_250 (lowest that works with audio)

* Mon Jul 14 2008 Thomas Backlund <tmb@mandriva.org> 2.6.25.11-1mdv
- update to 2.6.25.11

* Sun Jul  6 2008 Thomas Backlund <tmb@mandriva.org> 2.6.25.10-1mdv
- update to 2.6.25.10
- update patch DS01: Alsa 1.0.17rc3
- rediff patch RT01: realtime support

* Mon Jun 30 2008 Thomas Backlund <tmb@mandriva.org> 2.6.25.9-3mdv
- add patch DM50: v4l-dvb tree as of 2008-06-29
- add patch DM51: v4l-dvb compat fixes for 2.6.25
- update patch MB10, MB12: ndiswrapper 1.53
- add patch MC82: add missing viahss MODULE_LICENSE
- re-enable patch MD01: uvc buildfix due to new v4l-dvb code in patch DM50
- add patch RT01: realtime support v 2.6.25.8-rt7 (for realtime flavour)
- add patch RT02: fix reiser4 build with -rt patchset
- add patch RT03: fix unionfs build with -rt patchset
- switch back to SLAB as SLUB does not work with -rt patchset
- disable netfilter ip_set, its broken with -rt patchset
- disable reiser4, its broken with -rt patchset
- disable RT2570 and QC-USB on -realtime flavours, as they
  do not work with full realtime
- enable build of -realtime flavour
- fix spec so the realtime kernels really gets built
- update defconfigs

* Sat Jun 28 2008 Thomas Backlund <tmb@mandriva.org> 2.6.25.9-2mdv
- fix patch DS02: to properly revert 2.6.26-rcX speciific code in 
  Alsa 1.0.17-rc2 (initial patch causes oops on boot :-( )

* Sat Jun 28 2008 Thomas Backlund <tmb@mandriva.org> 2.6.25.9-1mdv
- update to 2.6.25.9
- add support for -realtime flavour (disabled for now)
- drop patches merged upstream:
  * DA35_acpi-add-aliases-to-toshiba_acpi-module.patch
  * DA50_ata-ahci-ICH10-MCP7B-Marvell-ids.patch
  * DA51_ata-piix-ich10-ids.patch
  * DC01_fix-i8k-build-on-x86_64.patch
  * DC02_add-dell-mp061-support-to-i8k.patch
  * DC03_enable-i8k-on-x86_64-build.patch
  * DH02_hid-usbhid-blacklist.patch
  * DI10_input-tablet-wacom-0.7.9-8.patch
  * DI20_drivers-i2c_verify_client.patch
  * DM01_thinkpad-acpi-0.18-20071203_v2.6.24-rc6.patch
  * DM20_acpi-compal-laptop-20080205.patch
  * DM50_v4l-dvb-9a2af878cbd5-20080324.patch
  * DN10_net-r8169-fix-past-rtl_chip_info-array-size-for-unknown.patch
  * DN11_net-r8169-fix-oops-in-r8169_get_mac_version.patch
  * DN15_char-nozomi-driver.patch
  * DN40_net-forcedeth-locking-bug.patch
  * DN41_net-skge-napi-poll-locking-bug.patch
  * DN42_net-sky2-add-marvell-ids.patch
  * FP01_pagecache-zeroing-zero_user_segment-zero_user_segments-and-zero_user.patch
  * FP02_pagecache-zeroing-zero_user_segment-zero_user_segments-and-zero_user-fix.patch
  * FP03_pagecache-zeroing-zero_user_segment-zero_user_segments-and-zero_user-fix-2.patch
  * FR04_make-copy_from_user_inatomic-not-zero-the-tail-on-i386-vs-reiser4.patch
  * MB40_acer_acpi-0.11.1.tar
  * MB41_acer_acpi-Kconfig-Makefile.patch
- drop patches not needed anymore:
  * DI02_idedisk_reboot.patch
  * DN30_rndis_host_wm5-6.patch
  * KS01_kernel-sysctl_check-remove-s390-include.patch
  * MD01_3rd_uvc_buildfix.patch
- disable broken patches:
  * AS01_linux-phc-kernel-vanilla-2.6.25.8.patch
  * CR01_BadRAM-2.6.25.8.patch
  * FS10_fs-udf-2.50-from-2.6.26-rc1-git7.patch
- rediff patch DA21: asus_acpi Eee support
- rediff patch DB25: fix megaraid_mbox sysfs name
- rediff patch NI15: netfilter psd target
- replace old patches DS01-DS03 with new DS01: Alsa 1.0.17-rc2
- add patch DS02: revert 2.6.26 specific alsa code
- update patch DV01: bootsplash 3.1.6
- add patch MB21: fix squashfs build (from main)
- update patches MC30-MC32: drbd 8.0.12 (from main)
- update patch MC40: fsc_btns 1.10
- update patch MD10: fix Prism25 Kconfig
- update patch FS01: unionfs 2.3.3
- update patch KP01: TuxOnIce 3.0-rc7
- update defconfigs
- fix -doc filelist
- do not remove modules.* before calling depmod in install 
  (fixes missing modules.order file, noted by Anssi)
- dont ship mn10300 arch files
- add arch/Kconfig to -devel and -source rpms
- add /virt to -source rpm
- remove unlinking of /arch/i386/boot/bzImage, not needed anymore

* Sat Jun 21 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24.7-3mdv
- fix build with disabled -doc
- fix -doc versioning
- update patch DA50: Ahci ICH10 MCP7B Marvell ids 
- add patch DA51: add ich10 support to ata_piix
- add patch DA52: add Tecra M4/M6 and Satellite R20 to piix_broken_suspend
- add patch DN40: fix forcedeth locking bug
- add patch DN41: fix skge locking bug
- add patch DN42: add more Marvell ids to sky2
- add dvb-core header files to -devel rpms so it's possible to build
  external dvb drivers without needing full source (#41418)

* Fri May 23 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24.7-2mdv
 - bump release to 2mdv to get past testing kernels
 
* Sun May 11 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24.7-1mdv
- update to kernel.org 2.6.24.7: fix CVE-2008-1669
- move patch DA10 (add ata ids) to DA50 to make room for more acpi fixes
- add patches from main kernel:
  * DA10-DA12: acpi wmi interface
  * DA15: acpi proc event regs
  * DA20: Generate input events for ACPI hotkeys in asus-laptop
  * DA21-DA22: add Acpi eee support
  * DA25: disable acpi_irq on CLEVO M360S
  * DA26: limit Clevo M720SR to C2 power state as C3 causes lockup
  * DA30: make acpi video ignore unsupported devices
  * DA35: add ids to toshiba_acpi to enable autoloading
- drop patches DS90-DS91: serial-wacom-acpi, it's broken and replaced by
  acpi-wmi patches DA10-DA12
- update patch FS10: UDF 2.50 from 2.6.26-rc1-git7, fixes memory corruption
  (exportfs part reverted to get a clean backport for main)
- update patch MD00: uvc r205 (from main)
- update patch MD01: uvc buildfixes to match v4l-dvb patch DM50
- update defconfigs

* Tue May  6 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24.6-2mdv
- add patch DA10: add device ids for Intel ICH10, nVidia MCP7B and
  Marvell 6121 to SATA AHCI
- update patch DS02: Alsa HG Snapshot 2008-05-04
- replace old patch FS10: new clean backport of UDF2.5 from 2.6.26-rc1
- add fixes from main kernel:
    * DN10: r8169: fix past rtl_chip_info array size for unknown chipsets
    * DN11: r8169: fix oops in r8169_get_mac_version
    * DS03: dont build pcspkr when snd-pcsp is enabled as they conflict

* Sat May  3 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24.6-1mdv
- update to kernel.org 2.6.24.6
  * fixes CVE-2008-1375, CVE-2008-1675
  * http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.24.6
  * http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.24.5
- rediff patd DM50:. v4l_dvb snapshot
- update patch FS01: unionfs 2.3.3
- add patch FS10: UDF v2.5 support (#40412)
- update patch KP01: Suspend2 3.0-rc7
- enable CONFIG_FS_UFS_WRITE

* Tue Mar 25 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24.4-1mdv
- update to 2.6.24.4:
  * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.24.4
- drop patches AA01-AA14: patches from stable tree (merged upstream)
- add patch DI20: add i2c_verify_client support (needed for v4l-dvb)
- add patch DM50: upstream v4l-dvb snapshot as of 20080324
- drop patches DS01-DS03, DS11-DS76, DS99: alsa fixes from Alsa HG
- rediff and rename patch DS10 to DS01: alsa 1.0.16 final
- add patch DS02: Alsa HG 20080323 full checkout
- fix patch DS02 to actually build on i586
- rediff patch FP01: pagecache zeroing fixes
- Include bttv.h and bttvp.h headers in kernel-devel, required by
  dkms-lirc-gpio (#39004, patch by Anssi Hannula <anssi@mandriva.org>)
- Fix kernel-source symlinks if the kernel is installed after the
  source and no matching -devel- rpm is installed (#38862)
- update defconfigs
- fix license

* Sun Mar  9 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24.3-4mdv
- override system buildroot definition on 2008 systems to 
  get back correct BuildRoot behaviour
- add patches from upstream stable queue:
  * AA01: ipcomp-disable-bh-on-output-when-using-shared-tfm
  * AA02: ipconfig-the-kernel-gets-no-ip-from-some-dhcp-servers
  * AA03: ipv4-remove-ip_tos-setting-privilege-checks
  * AA04: ipv6-dst_entry-leak-in-ip4ip6_err
  * AA05: ipv6-fix-ipsec-datagram-fragmentation
  * AA06: net-fix-race-in-dev_close
  * AA07: net-messed-multicast-lists-after-dev_mc_sync-unsync
  * AA08: niu-bump-driver-version-and-release-date
  * AA09: niu-fix-bmac-alternate-mac-address-indexing
  * AA10: niu-more-bmac-alt-mac-address-fixes
  * AA11: revert-net-add-if_addrlabel.h-to-sanitized-headers
  * AA12: sparc64-loosen-checks-in-exception-table-handling
  * AA13: sparc-fix-link-errors-with-gcc-4.3
  * AA14: tcp-improve-ipv4-established-hash-function
- add updates from Alsa HG:
  * DS02: pcsp: improve "enable" option handling
  * DS04: pcsp: add description
  * DS69: hda-codec - model for alc883 to support FUJITSU Pi2515
  * DS70: hda-codec - model for cx20549 to support laptop HP530
  * DS71: hda_intel: Add the IDs of nvidia MCP79 HD audio controller
  * DS72: hda-codec - Fix dmics on ALC268 in auto configuration
  * DS73: hda-codec - Add internal mic item for ALC268 acer model
  * DS74: HDA Codecs: add support for Toshiba Equium L30
  * DS75: at73c213: fix error checking for clk API
  * DS76: at73c213: monaural support
- add patch FF01: fix timestamps on fat partitions (#26819)

* Wed Mar  5 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24.3-3mdv
- add patch DV01: bootsplash 3.1.6 
- add Provides should-restart = system
- add patch DH02: fix for wacom serial devices when usbhid are loaded (#35201)
- update patch DN30: full usb-rndis-lite svn rev 3305 checkout (#30128)
- replace old patches DS01-DS03 with new DS01,DS02:
  * alsa pc-speaker support from Alsa HG
- add fixes from Alsa HG tree:
  * DS67: hda-codec mode for alc883 to support M720R
  * DS68: hda ALC288 Add NEC S970 to the quirk table
- add patches DS90,DS91: Enable a wacom digitizer on an HP TC1100
- update patch KP01: TuxOnIce 3.0-rc5
- add patch MB65: ipw3945 fix skb->tail on 64 bit
- update defconfigs

* Sun Mar  2 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24.3-2mdv
- update patch DI10: wacom tablet 0.7.9-8 (#37073)
  * bugfixes, adds support for Wacom Cintiq 20WSX
- add patch DH01: add usb hid quirk for Multilaser USB-PS/2 
  keyboard adapter (#36870)
- add fixes from Alsa HG tree:
  * DS53: hda-codec adapt eeepc p701 mixer for virtual master control
  * DS54: usb-audio add workaround for broken E-Mu frequency feedback
  * DS55: usb-audio sort quirks list
  * DS56: sb8 fix sb 1.0 capture DMA programming
  * DS57: hda-codec fix AD1988 capture elements
  * DS58: hda-codec add Fujitsu Lifebook E8410 to quirk table
  * DS59: hda-codec fix initial DAC numbers of 92HD71bxx codecs
  * DS60: oxygen add owner field
  * DS61: hda-codec add docking-station mic-input for Thinkpad X61
  * DS62: hda-codec fix names of realtek codecs to adapt master controls
  * DS63: intel8x0 add quirk for Compaq Deskpro EN
  * DS64: hda-sigmatel disable power management on fixed ports
  * DS65: hda-sigmatel-add-verbs-for-92hd73xxx-laptops
  * DS66: hda-codec fix array over-range access with stac92hd71bxx codec

* Fri Feb 29 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24.3-1mdv
- update to 2.6.24.3 stable:
  * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.24.3
- update patch MB40: acer_acpi 0.11.1
- add patch MD10: Prism2 v0.2.9 (#38155)
- update defconfigs

* Sat Feb 23 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24.2-2mdv
- disable CONFIG_USB_OHCI_HCD_SSB so ssb wont get loaded even if it
  is blacklisted (reported by AdamW on kernel-discuss)
- disable FAIR_USER_SCHED and FAIR_GROUP_SCHED to get better
  porformance from the kernels (reported by FHimpe on kernel-discuss)
- add patch DI10: update Wacom tablet support (#37073)
  * adds support for: Bamboo1, BambooFun and Cintiq 12WX
- add patch DM20: add compal-laptop driver (#37860)
- add patch DN30: initial rndis wm5/6 support (#30128)
- add more fixes and addons from Alsa HG:
  * DS24: sound-hda-codec-fix-ALC880-F1734-model
  * DS25: sound-hda-codec-fix-automute-of-AD1981HD-hp-model
  * DS26: sound-hda-codec-dont-create-vmaster-if-no-slaves-found
  * DS27: sound-hda-codec-fix-wrong-capture-source-selection-for-ALC883-codec
  * DS28: sound-hda-codec-fix-ALC882-capture-source-selection
  * DS29: sound-hda-codec-clean-up-capture-source-selection-of-Realtek-codecs
  * DS30: sound-hda-codec-implement-auto-mic-jack-sensing-for-Samsung-laptops-with-AD1986A
  * DS31: sound-hda-codec-more-auto-configuration-fixups
  * DS32: sound-hda-codec-fix-aout-configuration-of-realtek-codecs
  * DS33: sound-hda-codec-add-IEC958-default-PCM-switch
  * DS34: sound-hda-codec-add-more-names-to-vendor-list
  * DS35: sound-hda-codec-fix-breakage-of-resume-in-auto-config-of-realtek-codecs
  * DS36: sound-hda-intel-add-ATI-RV7xx-HDMI-audio-support
  * DS37: sound-hda-codec-fix-amp-in-values-for-pin-widgets
  * DS38: sound-hda-codec-fix-missing-capsrc_nids-for-ALC262
  * DS39: sound-hda-codec-add-support-for-AD1883-AD1884A-AD198A-q984B
  * DS40: sound-hda-codec-add-model-mobile-for-AD1884A
  * DS41: sound-intel8x0-add-support-for-8-channel-sound
  * DS42: sound-hda-codec-fix-master-volume-on-HP-dv8000
  * DS43: bt87X-fix-freeing-of-shared-interrupt
  * DS44: sound-hda-intel-fix-oops-with-ATI-HDMI-devices
  * DS45: sound-hda-codec-fix-ALC662-recording
  * DS46: sound-hda-codec-fix-ALC268-capture-source
  * DS47: sound-hda-codec-fix-STAC927x-power-management
  * DS48: sound-hda-codec-fix-STAC927x-invalid-association-value
  * DS49: sound-hda-add-PCI_QUIRKS-for-laptops-with-92HDxxxx-codecs
  * DS50: sound-hda-STAC927x-analog-mic
  * DS51: sound-seq_oss_synth-remove-invalid-bug
  * DS52: sound-hda-codec-add-missing-descriptions-for-STAC-codec-models
- update patch FS01: unionfs v2.2.4 (from main)
- update patch MB10: ndiswrapper 1.52
- update patch MC30: drbd v8.0.11 (from main)
- update patches MD00-MD01: uvc r173 (from main)
- update defconfigs
    
* Mon Feb 11 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24.2-1mdv
- quick update to 2.6.24.2 stable: (CVE-2008-0600)

* Sun Feb 10 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24.1-1mdv
- update to 2.6.24.1 stable:
  * CVE-2008-0007, CVE-2008-0009/10
  * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.24.1
- add patches DN20,DN21: Atheros L2 10/100 support
- update patch DS10: alsa 1.0.16 final
- add selected patches from alsa HG:
  * DS11: sound-soc-fix-duplicate-rj-master-test
  * DS12: sound-hda-intel-Fix-PCM-device-number-assignment
  * DS13: sound-hda-codec-Add-ID-for-HDMI-codec-on-Jetway-J9F2
  * DS14: sound-ice1712-Fix-hoontech-MIDI-input
  * DS15: sound-hda-STAC927x-power-down-inactive-DACs
  * DS16: sound-hda-intel-use-SG-buffers
  * DS17: sound-hda-intel-support-64bit-buffer-allocation
  * DS18: sound-ice1712-add-support-for-Delta-1010E
  * DS19: sound-ice1712-all-support-for-Delta-66E
  * DS20: sound-hda-intel-Fix-compile-error-with-CONFIG_SND_DEBUG_DETECT
  * DS21: sound-hda-codec-correct-HDMI-transmitter-names
  * DS22: sound-hda-codec-remove-duplicate-controls-in-alc268-test-mixer
  * DS23: sound-hda-codec-Fix-race-condition-in-generic-bound-volume-switch-controls
- update defconfigs

* Fri Feb  1 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24-2mdv
- add patch DM10: device-mapper raid4/5 target
- add patch DM11: fix device-mapper  raid4/5 build for 2.6.24
- update patch DN15: nozomi driver merged upstream
- drop patch DN16: nozomi build fix, not neede anymore
- uppdate patch DS10: alsa 1.0.16rc2 + git-2008-01-31
- add patch KS01: disable inclusion of s390 file in sysctl_check as 
  we dont ship arch/s390 files in our kernel-source (#37388)
- update defconfigs

* Sat Jan 26 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24-1mdv
- update to 2.6.24 final
- drop patch KS01: CFS cpu_share fix (merged upstream)
- update patch FS01: unionfs 2.2.3

* Wed Jan 23 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24-0.rc8.2mdv
- update to 2.6.24-rc8-git5
- add patch DS10: alsa 1.0.16-rc1
- add patch KS01: CFS cpu_share tunable crash fix (LKML)
- update defconfigs

* Sat Jan 19 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24-0.rc8.1mdv
- update to 2.6.24-rc8-git3
- rediff patch CR01: BadRAM support
- drop patch DA01: acpi regression fixes (merged upstream)
- update FR01-FR17: Reiser4 support (from 2.6.24-rc8-mm1)
- update FS01: unionfs 2.2.2
- set CONFIG_PHYSICAL_START=0x200000 on x86_64 so the kernels actually boot
- make 32bit kernels conflict arch(x86_64) so they cant be installed
  by mistake (#32631)
- update defconfigs

* Sat Jan 12 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24-0.rc7.4mdv
- update to 2.6.24-rc7-git4
- add patch DA01: acpi-release-20070126-2.6.24-rc7, acpi regression
  fixes (should fix #36711)
- disable XEN Guuest support on all but server kernels as it 
  breaks AGP support (#36458)

* Thu Jan 10 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24-0.rc7.3mdv
- update to 2.6.24-rc7-git2
- drop patch DS05: alsa hda_intel revert (merged upstream)

* Wed Jan  9 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24-0.rc7.2mdv
- redo the defconfigs as they got somewhat screwed up in last build
- add patch DS05: revert alsa hda_intel to -rc6 status as -rc7 is broken
  (noted on LKML)
- disable CONFIG_RTC as it conflicts with GEN_RTC

* Mon Jan  7 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24-0.rc7.1mdv
- update to kernel.org 2.6.24-rc7
- review and updeate defconfigs
  * make RTC modular (same as main kernel)
  * enable USB_SUSPEND and USB_PERSIST
  * enable some modules that got disabled by mistake
- fix url to point at Mandriva wiki

* Sat Jan  5 2008 Thomas Backlund <tmb@mandriva.org> 2.6.24-0.rc6.3mdv
- update to kernel.org 2.6.24-rc6-git11
- update patch FS01: unionfs 2.2.1
- more spec fixes due to x86 merge
- fix build,source symlinks to -source tree to be created only if no
  matching -devel tree is installed, and to be removed only if they
  point at the -source tree
- optimize NR_CPUS according to flavours for memory savings
  * desktop586: 8, desktop: 16, laptop: 8, server: 32

* Mon Dec 31 2007 Thomas Backlund <tmb@mandriva.org> 2.6.24-0.rc6.2mdv
- update to kernel.org 2.6.24-rc6-git7
- Doh :-( ... re-enable SMP support in all configs as it got disabled by
  mistake in the scripts cleanup

* Sun Dec 30 2007 Thomas Backlund <tmb@mandriva.org> 2.6.24-0.rc6.1mdv
- add support for -git tarballs
- update to 2.6.24-rc6-git6
- rediff patch AI01: Toshiba Equium A60 needs pci=assign-busses
- drop patches AI02-AI03: picopower irq-router support (merged upstream)
- rediff patch AI10: error message suggesting use of desktop586 kernel
- drop patch AX01: nvidia sata corruption fix (fixed upstream)
- drop patch AX10: x86_64 High Resolution Timer & Tickless support
  (merged upstream)
- update patch AS01: linux-phc 0.3.1:1
- rediff patch CE02: acpi dsdt support
- drop patch CF01: CFS v24.1 (merged upstream)
- drop patches CK01-CK06: swap prefeth as upstream has dropped them too
- redo patch CR01: BadRAM support
- disable patches DA11-DA12: nVidia Software NCQ support, need to be redone
- drop patch DA81: Danny's Intel HDA codec detection fix, merged upstream
- redo patch DC03: fix Kconfig to enable i8k on x86_64
- update patch DM01: thincpad-acpi v 0.18 for 2.6.24-rc6
- drop patch DN20: iwlwifi support, merged upstream
- add patch DS03: pcsp buildif for 2.6.24
- add patches FP01-FP03: add pagecache zero_user* support, needed for reiser4
- replace old patches FR01-FR22 with new FR01-FR22: Reiserfs4 support from
  AKPM's 2.6.24-rc6-mm1
- update patch FS01: unionfs v 2.2
- update patch KP01: tuxonice v 3.0-rc3
- update patch MB02: 3rdparty merge (from main)
- update patch MB20: squashfs 3.3
- drop patches MB21-MB23: squashfs fixes (not needed anymore)
- add patch MB32: acerhk buildfix for 2.6.24
- update patches MB50-MB52: qc-usb v 0.6.6
- add patch MB64: ipw3945 buildfix for 2.6.24
- add patch MB72: rt2400 buildfix for 2.6.24
- add patch MB82: rt2500 buildfix for 2.6.24
- add patch MB92: rt2570 buildfix for 2.6.24
- add patch MC03: rt61 buildfix for 2.6.24
- add patch MC13: rt73 buildfix for 2.6.24
- add patch MC53: acx buildfix for 2.6.24
- update patch MD00-MD02: uvc r158 (from main)
- drop patch MS02: SLUB regression fix, merged upstream
- updste patches NI01-NI05: ipset support (from main)
- update patches NI10-NI11: ifwlog support (from main)
- update patches NI15-NI16: psd support (from main)
- disable patches SA01-SA58: AppArmor support, need to be updated
- update specfile & build scripts for the i386 + x86_64 > x86 merge
- drop defconfig-maximum as it's a duplicate of defconfig-desktop
- use make clean on -devel & source tree to not ship unneeded files
- update defconfigs
- drop README.urpmi

* Fri Dec 28 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23.12-2mdv
- update patches DS01-DS02: alsa pcspeaker support, and enable it
- update patches MB10-MB12: ndiswrapper 1.51

* Mon Dec 24 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23.12-1mdv
- update to kernel.org 2.6.23.12 stable:
  * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.23.12
- update patch CF01: CFS scheduler v 24.1
- drop patches CF02-CF04: CFS bugfixes (merged upstream)
- add patch DM01: update to thinkpad-acpi v 0.18 (#35222)
- update patch MB40: acer_acpi 0.10 final
- add patch MS01: fix SLUB vs SLAB hackbench regression
- switch to SLUB as default (same as upstream)
- update defconfigs

* Sun Dec 16 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23.11-1mdv
- update to kernel.org 2.6.23.11 stable:
  * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.23.11

* Sat Dec 15 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23.10-1mdv
- update to kernel.org 2.6.23.10 stable:
  * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.23.10
- drop patches AA01-AA08: -stable prepatches (merged upstream)
- add patch AI10: fix kernel error message when CPU is not fully
  i686-compatible, and suggest desktop586 flavour (#34231)
- rediff patch CF01: CFS scheduler v24
- add patch CF04: sched: enable early use of sched_clock()
- update patch MB40: acer_acpi 0.10rc5
- update patch MC30: drbd v 8.0.8 (#36055)

* Tue Dec  4 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23.9-3mdv
- add patches CF02, CF03: CFS scheduler Local Dos bugfixes (#35822)

* Sun Dec  2 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23.9-2mdv
- add patches AA01-AA08 from stable queue:
  * libertas: properly account for queue commands
  * NET: random : secure_tcp_sequence_number should not assume 
    CONFIG_KTIME_SCALAR
  * NETFILTER: Fix NULL pointer dereference in nf_nat_move_storage()
  * ramdisk: fix data corruption on memory pressure
  * PKT_SCHED: Check subqueue status before calling hard_start_xmit
  * Fix synchronize_irq races with IRQ handler
  * Input: ALPS - add support for model found in Dell Vostro 1400
  * Input: ALPS - add signature for ThinkPad R61

* Wed Nov 28 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23.9-1mdv
- update to kernel.org 2.6.23.9:
  * CVE-2007-5500, CVE-2007-5501, CVE-2006-6058
  * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.23.9
  * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.23.8
  * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.23.7
  * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.23.6
  * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.23.5
  * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.23.4
  * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.23.3
  * http://www.eu.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.23.2
- update patch CF01: CFS scheduler to v24
- add patch DN20: iwlvifi 1.2.0
- update patch MB10: ndiswrapper 1.49 final
- update patch MB40: acer_acpi 0.10rc4
- add patch NI07: netfilter IFWLOG api fix (Luiz)
- add patch NI12: netfilter PSD api fix (Luiz)
- sync with main:
  * update patches MB70-MB71: rt2400 cvs20071020 wireless support
  * update patches MB80-MB81: rt2500 cvs20071020 wireless support
  * update patches MB90-MB91: rt2570 cvs20071020 wireless support
  * update patches MC00-MC02: rt61 cvs202071020 wireless support
  * update patches MC10-MC12: rt73 cvs20071020 wireless support
  * add patches MC50-MC52: acx cvs200701 wireless support
  * add patches MC60-MC51: Atmel at76c503a wireless support
  * add patches MC80-MC81: Via High Speed serial support
  * add patch MD00: USB Video class support
- enable DEBUG_BUGVERBOSE for x86_64 too
- update defconfigs

* Tue Oct 30 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23.1-2mdv
- add patches DC01-DC03: fix x86_64 build of i8k (Dell SMM)

* Sat Oct 20 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23.1-1mdv
- update to kernel.org 2.6.23.1 stable
- drop patch AA01: 2.6.23-rc8-git2, merged upstream
- update kernel-laptop summary and descriptions
- update patch AX10: High Resolution Timer Support & Tickless System
  to 2.6.23-hrt3
- add patch CF01: update CFS scheduler to v22.1-rc0
- update patch MB10: ndiswrapper-1.49rc4
- update patch MB40: acer_acpi 0.10rc3
- update patches MB60-MB64: ipw3945 1.2.2
- sync wireless support with main:
  * update MB70,MB71: rt2400-cvs20070820
  * update MB80,MB81: rt2500-cvs20070820
  * update MB90,MB91: rt2570-cvs20070820
  * update MC00-MC02: rt61-cvs20070820
  * update MC10-MC12: rt73-cvs20070823
- add patches MC40,MC41: Tablet Buttons Driver for Fujitsu Siemens
  (requested bu Austin)
- re-enable CONFIG_INPUT_TABLET as it got disabled by mistake
- set -laptop kernels to HZ_300 as HZ_100 is known to cause audio skips
  as noted during testing of main kernel
- disable mrproper target on -devel rpms to stop 3rdparty installers from 
  wiping out needed files and thereby breaking builds
  (based on an initial patch by Danny used in kernel-multimedia series)
- update defconfigs

* Fri Sep 28 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23-0.rc8.1mdv
- update to kernel.org 2.6.23-rc8-git2 (fixes CVE-2007-4571)
- drop old patch AA01: CVE-2007-4573 fix, merged upstream
- drop patches AA10, AA11: ACPI and VESA wakeup fixes, merged upstream
- rediff patch AX10: hrt/tickless support

* Sun Sep 23 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23-0.rc7.2mdv
- add patch AA01: x86_64 zero extend all registers after ptrace in 
  32bit entry path (CVE-2007-4573)
- add patch SA48: fix AppArmor return-code and rejected_mask 
  (from John Johansen @ suse)
- add patch FS03: unionfs: do not update mtime if there is no upper 
  branch for the inode (blino@mandriva.com)

* Thu Sep 20 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23-0.rc7.1mdv
- update to kernel.org 2.6.23-rc7
- drop patch AA01: rc6-git6, mergesd upstream
- add patch AA10: fix VESA mode decoding in ACPI wakeup (LKML)
- add patch AA11: fix ACPI wakeup devices after hibernation (LKML)
- update patch AX10: High Resolution Timer Support & Tickless System
  2.6.23-rc7-hrt1
- add patch MC32: drbd Kconfig and Makefile buildfix (from main, Luiz)
- rediff patch KP01: tuxonice 2.2.10.3
- require the fixed mkinitrd-4.2.17-52mdv
- fix i386 defconfig to be i686, so that only desktop586 is built
  for i586 (Thanks to Danny for noticing)
- update defconfigs

* Thu Sep 20 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23-0.rc6.2mdv
- update patch KP01: tuxonice 2.2.10.3 (suspend2) is back
- update defconfigs

* Sun Sep 16 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23-0.rc6.1mdv
- update to kernel.org 2.6.23-rc6
- update patch AA01: 2.6.23-rc6-git6
- update patch AX10: High Resolution Timer Support & Tickless System
  2.6.23-rc6-hrt2
- update patches FS01, FS02: unionfs 2.1.3
- add patch SA47: fix AppArmor syslog logging (AppArmor svn rev 961)
- update defconfigs

* Thu Sep  6 2007 Thomas Backlund <tmb@mandriva.org> 2.6.23-0.rc5.1mdv
- update to kernel.org 2.6.23-rc5
- add patch AA01: 2.6.23-rc5-git1
- update patch AX10: High Resolution Timer Support & Tickless System
- disable patch CA03: video 80x25 fallback, as there is a brand new
  setup code in 2.6.23-rcX
- drop patch CF01: cfs sceduler, merged upstream
- disable patches CK01-CK06: swap prefetch as it's broken
- drop patches DA59-DA80: alsa fixes, merged upstream
- drop patch DC01: P4M900 agpgart spport, merged upstream
- drop patch DF01: dmi based autoloading, merged upstream
- drop patch DI01: 2.6.23-ide-git-upstream, merged upstream
- drop patch DI10: wacom bamboo support, merged upstream
- drop patches DI25,DI26: marvell ide support, as it's broken
- disable patch DN02: add 47xx support to b44, needs to be updated
- drop patch DN03: forcedeth phy oui id fix, merged upstream
- disable patch DN04: e1000 update, needs to be updated
- drop patch DN05: r8169 link down fix, merged upstream
- drop patched DN50-DN52: wireless (dscape) git
- drop patches DS11, DS12: Amd SB700/800 smbus support, mreged upstream
- drop patch DV01: fbsplash support
- drop patches DV21, DV22: nvidiafb fixes, merged upstream
- update/add patches FR01-FR22: ReiserFS4 from 2.6.23-rc4-mm1
- update patch FS01: unionfs 2.1.2 for 2.6.23-rc3
- rediff patch FS02: unionfs AppArmor buildfix
- drop patches FS04, FS05: ext3/4 orphan list debug support and 
  corruption fix, merged upstream
- disable patch KP01: suspend2 support, as upstream needs to catch up
- update patch MB10: ndiswrapper 1.48-rc2
- redo patch MB11: ndiswrapper Kconfig & Makefile fix
- add patch MB23: squasfs buildfix for 2.6.23
- update patch MB40: acer_acpi v0.8.2
- update patch MC30: drbd 8.0.6
- disable  patch NB01: bluetooth sco support, need to be rewritten
- add patch NI02: ipset 2.6.23 buildfix
- rediff patches SA03, SA21: AppArmor
- add include/xen/ to filelists
- update defconfigs

* Tue Sep  4 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22.6-2mdv
- add patch DA81: alsa hda-intel codec detection fix (Danny)
- enable USB_SUSPEND only on laptop kernels, as it causes to much 
  regressions for normal users, but is a tradeoff for laptop users (#33089)
- add patches FS04, FS05: ext3/4 orphan list debug support and corruption 
  fix (#32527) (main kernel, Luiz)
- make SUSPEND2 builtin on -laptop kernels as it cant resume without it

* Sat Sep  1 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22.6-1mdv
- update to kernel.org 2.6.22.6:
  * fixes: http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.22.6
- drop patch AA01: merged upstream
- update patch AS01: linux-phc 0.3.0
- update patch CF01: CFS v 20.5
- redo patch FS02: unionfs AppArmor vfs uildfix (initial patch for
  2.1 by John Johansen <jjohansen@suse.de>
- readd patch NI05: netfilter IFWLOG support
- add patch NI06: IFWLOG buildfix for 2.6.22
- readd patch NI10: netfilter PSD support
- add patch NI11: PSD buildfix for 2.6.22
- update patches SA01-SA46: AppArmor 2.1 prerelease
  (SuSe 10_3 branch, commit 942)
- enable DEBUG_FS (#32886)
- enable USB_EHCI_TT_NEWSCHED (#32894)
- fix #29744, #29074 in a cleaner way by disabling the sourcing of
  arch/s390/crypto/Kconfig
- update defconfigs

* Sun Aug 26 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22.5-2mdv
- add patch AA01: 2.6.22.6-rc1
- update patch CF01: CFS v 20.4
- add patch DC01: add Via P4M900 agpgart support
- drop patches DN33-DN43: old netfilter ipset, ifwlog, psd support
- update patch MB40: acer_acpi v0.7
- redo patch MB41: fix acer_acpi Kconfig and Makefile
- add patch NI01: netfilter ipset support (from OpenWrt) (#32399)
- make CPU_IDLE_GOV_MENU builtin on -laptop kernels (Request by Danny)
- update defconfigs

* Fri Aug 24 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22.5-1mdv
- update to kernel.org 2.6.22.5:
  * fixes CVE-2007-3848
  * other fixes: http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.22.5
- update patch CF01: CFS scheduler v 20.2
- drop patch CF02: CFS updates, merged upstream
- drop patch CK07: merged in CFS
- drop patch DB33: sb700 ahci support, merged upstream
- update patch FS01: unionfs 2.1.2
- update defconfigs
 
* Fri Aug 17 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22.3-1mdv
- update to kernel.org 2.6.22.3:
  * fixes: CVE-2007-3105 and other bugs
  * full log: http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.22.3
- add audio fixes from main kernel:
    DA59_hda_codec_fix_51_output.patch
    DA60_hda_codec_hp_spartan_quirk.patch
    DA61_usbaudio_roland_junog_quirk.patch
    DA62_hda-codec-hp-nettle-id.patch
    DA63_hda-codec-fix-hp-nettle-51.patch
    DA64_hda-codec-hp-lucknow-51-support.patch
    DA65_hda-codec-Add-quirk-for-HP-Samba.patch
    DA66_hda-codec-Add-LG-LW20-line-in-capture-sourc.patch
    DA67_hda-codec-Add-LG-LW20-si3054-modem-id.patch
    DA68_hda-codec-Add-quirks-for-HP-dx2200-dx2250.patch
    DA69_si3054.patch
    DA70_hda-codec-Add-quirk-for-Asus-P5LD2.patch
    DA80_usbaudio-logitech-id.patch
- add network updates from main kernel:
    DN01_r8169_link_down_fix.patch
    DN02_e1000_7.6.5.patch
    DN03_fix-forcedeth-phy-oui-realtek-id.patch
- add ide/ahci updates from main kernel:
    DB33_ahci_SB700_support.patch
    DI25_add_marvell_ide.patch
- add smbus updates from main kernel:
    DS01_smbus_sb700_support.patch
    DS02_smbus_sb800_support.patch
- add patch DI26: fix marvell ide to build with 2.6.22+
- update patch FS01: unionfs 2.1
- redo patch FS02: fix unionfs to build with AppArmor
- update defconfigs
  
* Fri Aug 10 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22.2-1mdv
- update to kernel.org 2.6.22.2:
  * fixes: CVE-2007-3851 and other bugs
  * full log: http://www.kernel.org/pub/linux/kernel/v2.6/ChangeLog-2.6.22.2
- rediff patch AX10: High Resolution Timer Support & Tickless System
- drop patch DA15: Intel Santa Rosa support, merged upstream
- update patch DI10: wacom bamboo to add missing define
- update patch MB11: add missing KSRC parameter to ndiswrapper Makefile
- rediff patch SA03: AppArmor vfs-notify_change

* Sun Jul 15 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22.1-2mdv
- update patch AX10: High Resolution Timer Support & Tickless System
  to 2.6.22-hrt6
- add patch CF02: CFS scheduler updates (from -rt tree)
- update patch FS01: unionfs 2.0 2.6.22.1-u2
- refiff patch FS02: unionfs AppArmor buildfix
- use readlink instead of ls and awk in scripts, as ls broken in
  current coreutils (#31906), this also makes the scripts nicer

* Fri Jul 13 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22.1-1mdv
- update to kernel.org 2.6.22.1:
  * NETFILTER: {ip, nf}_conntrack_sctp: fix remotely triggerable
    NULL ptr dereference (CVE-2007-2876)
- update patch AX10: High Resolution Timer Support & Tickless System
  to 2.6.22-hrt2
- update patch CF01: Ingo Molnar's CFS-v19 Scheduler for 2.6.22.1
- add patch DN50: mac80211 (dscape) wireless drivers
  * ADMtek ADM8211
  * Broadcom BCM43xx
  * Iwlwifi
  * Prism64 PCI, USB
  * Ralink rt2400, rt2500, rt2500 usb, rt61, rt73
  * Realtek 8187 USB
  * ZyDAS ZD1211/ZD1211B USB
- add patch DN51: update mac80211 iwlwifi to 0.1.1
- add patch DN52: add missing parts to get dscape drivers to build
- update patch MB40: acer_acpi v0.6
- drop patch MC20: 3rdparty iwlwifi driver (replaced by DN50, DN51)
- update defconfigs

* Tue Jul 10 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-2mdv
- update patch AX10: High Resolution Timer Support & Tickless System
  to 2.6.22-hrt1
- update patch CF01: Ingo Molnar's CFS-v19 Scheduler for 2.6.22
- add patch DF01: dmi based module autoloading
- add patch DI01: IDE updates from upcoming 2.6.23-rc1
- add patch DI10: Add Wacom Bamboo Tablet support (#31831)
- add patch DV21: add proper support for geforce 7600
- add patch DV22: modify nvidiafb to use a faster scroll method
- update defconfigs

* Mon Jul  9 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-1mdv
- update to kernel.org 2.6.22 final
- drop patch AA01: merged upstream

* Sun Jul  8 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc7.2mdv
- update patch AA01: kernel.org 2.6.22-rc7-git6
- update patch AX10: High Resolution Timer Support & Tickless System
  to 2.6.22-rc7-hrt1
- update patch CF01: Ingo Molnar's CFS-v19 Scheduler for 2.6.22-rc7
- add patch CK01: Swap Prefetch
- replace patch CK01 with patches CK01-CK07: Enhanced Swap Prefetch
  from 2.6.22-rc6-mm1
- make kernel-source provide kernel-devel again until we figure out 
  what to do with dkms & co
- update defconfigs

* Tue Jul  3 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc7.1mdv
- update to kernel.org 2.6.22-rc7
- add patch AA01: 2.6.22-rc7-git1
- rediff patch SA03: AppArmor vfs-notify change

* Sun Jul  1 2007 Thomas Backlund <tmb@mandriva.org> 2.6.22-0.rc6.2mdv
- update patch AX10: High Resolution Timer Support & Tickless System
  to 2.6.22-rc6-hrt1
- add patches MC31, MC31: drbd 8.0.4
- make kernels provide drbd-api 86 (AdamW request)
- update patches SA01-SA44: AppArmor 2.0.2 build 755
- kernel-source does not provide kernel-devel anymore
- add patches DA10,DA11: add NCQ support to sata_nv for MCP51/55/61
- add patch DA15: add ich8m ata support
- update patches DN15,DN16: Nozomi 3G driver
- add patches FR01-FR12: Reiser4 filesystem
  - rediff patch FR01: to actually make it work
  - drop patches FR07, FR12: -mm specific code
- add patch KP01: Suspend2 2.2.10.2 support
- update patches SA01-SA45: AppArmor 2.0.2 build 755
- update defconfigs

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
