%define compiler_family gnu

#-fsp-header-comp-begin-----------------------------

# Compiler dependencies
BuildRequires: lmod coreutils
%if %{compiler_family} == gnu
BuildRequires: FSP-gnu-compilers 
Requires:      FSP-gnu-compilers 
%endif
%if %{compiler_family} == intel
BuildRequires: gcc-c++ FSP-intel-compilers 
Requires:      gcc-c++ FSP-intel-compilers 
%if 0%{?FSP_BUILD}
BuildRequires: intel_licenses
%endif
%endif

#-fsp-header-comp-end-------------------------------

# Base package name
%define pname metis
%define PNAME %(echo %{pname} | tr [a-z] [A-Z])

Name: %{pname}-%{compiler_family}
Summary: Serial Graph Partitioning and Fill-reducing Matrix Ordering
Version: 5.1.0
Release: 1
License: BSD-like
Group:   Productivity/Graphics/3D Editors  
URL: http://glaros.dtc.umn.edu/gkhome/metis/metis/overview
Source0: %{pname}-%{version}.tar.gz
Source1: FSP_macros
Source2: FSP_setup_compiler
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: make
BuildRequires: pkgconfig
BuildRequires: cmake
Requires:      libmetis0 = %{version}

%include %{_sourcedir}/FSP_macros

%define debug_package %{nil}

# Default library install path
%define install_path %{FSP_LIBS}/%{compiler_family}/%{pname}/%version

%description
METIS is a family of programs for partitioning unstructured graphs and hypergraph
and computing fill-reducing orderings of sparse matrices. The underlying algorithms
used by METIS are based on the state-of-the-art multilevel paradigm that has been
shown to produce high quality results and scale to very large problems.

%package -n libmetis0
Summary:        Serial Graph Partitioning and Fill-reducing Matrix Ordering
Group:          System/Libraries

%package devel
License:         Free for non-commercial use
Requires:        %name = %version
Requires:	 pkgconfig
Summary:         Metis development files
Group:           Development/Libraries/C and C++

%description -n libmetis0
METIS is a family of programs for partitioning unstructured graphs and hypergraph
and computing fill-reducing orderings of sparse matrices. The underlying algorithms
used by METIS are based on the state-of-the-art multilevel paradigm that has been
shown to produce high quality results and scale to very large problems.

%description devel
METIS is a family of programs for partitioning unstructured graphs and hypergraph
and computing fill-reducing orderings of sparse matrices. The underlying algorithms
used by METIS are based on the state-of-the-art multilevel paradigm that has been
shown to produce high quality results and scale to very large problems.

%prep
%setup -q -n %{pname}-%{version}
%build

# FSP compiler/mpi designation
export FSP_COMPILER_FAMILY=%{compiler_family}
. %{_sourcedir}/FSP_setup_compiler

make config shared=1 prefix=%{install_path}
make

%install

# FSP compiler/mpi designation
export FSP_COMPILER_FAMILY=%{compiler_family}
. %{_sourcedir}/FSP_setup_compiler

make install DESTDIR=${RPM_BUILD_ROOT}

# FSP module file
%{__mkdir} -p %{buildroot}%{FSP_MODULEDEPS}/%{compiler_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{FSP_MODULEDEPS}/%{compiler_family}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the %{PNAME} library built with the %{compiler_family} compiler toolchain."
puts stderr "\nVersion %{version}\n"

}
module-whatis "Name: %{PNAME} built with %{compiler_family} toolchain"
module-whatis "Version: %{version}"
module-whatis "Category: runtime library"
module-whatis "Description: %{summary}"
module-whatis "%{url}"

set     version			    %{version}

prepend-path    PATH                %{install_path}/bin
prepend-path    INCLUDE             %{install_path}/include
prepend-path	LD_LIBRARY_PATH	    %{install_path}/lib

setenv          %{PNAME}_DIR        %{install_path}
setenv          %{PNAME}_LIB        %{install_path}/lib
setenv          %{PNAME}_INC        %{install_path}/include

family "hdf5"
EOF

%{__cat} << EOF > %{buildroot}/%{FSP_MODULEDEPS}/%{compiler_family}/%{pname}/.version.%{version}
#%Module1.0#####################################################################
##
## version file for %{pname}-%{version}
##
set     ModulesVersion      "%{version}"
EOF

%post -n libmetis0
/sbin/ldconfig

%postun -n libmetis0
/sbin/ldconfig

%clean
rm -fr %buildroot

%files
%defattr(-,root,root)
%{FSP_HOME}
