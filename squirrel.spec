%define _disable_ld_no_undefined %{nil}

%define oname SQUIRREL2
%define packagedir SQUIRREL2

%define libname %mklibname %{name} %{version}
%define develname %mklibname %{name} -d

Name:		squirrel
Version:	2.2.5
Release:	9
Summary:	The squirrel language
License:	zlib
Group:		Development/Other
URL:		http://squirrel-lang.org
Source0:	http://ovh.dl.sourceforge.net/sourceforge/squirrel/%{name}_%{version}_stable.tar.gz
Source100:	squirrel.rpmlintrc
Patch0:         %{name}-2.2.5-fdr-autotools.patch
Patch1:         %{name}-2.2.4-fdr-mem.patch
Patch2:		squirrel-automake-1.13.patch

%description
Squirrel is a light weight programming language 
featuring higher-order functions,classes/inheritance,
delegation,tail recursion,generators,cooperative 
threads,exception handling, reference counting and 
garbage collection on demand. C-like syntax.

%package -n %{libname}
Summary:	Libraries for %{name}
Group:		Development/Other
Conflicts:	%{_lib}squirrel-devel < 2.2.5-2

%description -n %{libname}
Shared library files for %name.

%package -n %{develname}
Summary:	Header files and static libraries from %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 0 -d

%description -n %{develname}
Libraries and includes files for
developing programs based on %name.


%prep
%setup -qn %{oname}
%apply_patches

# fix file permissions
find . -type f -exec chmod a-x {} \;

# fix extension for autotools
mv sq/sq.c sq/sq.cpp

# fix EOL + preserve timestamps
for f in README HISTORY COPYRIGHT
do
    perl -pi -e 's/\015$//' $f
done

%build
sh autogen.sh

%configure2_5x --disable-static
%make

%install
%makeinstall_std INSTALL="/usr/bin/install -p"

rm %{buildroot}%{_libdir}/*.la

#correct wrong file end of line encoding 
perl -pi -e 's/\015$//' %{buildroot}/%{_includedir}/*

%files
%doc README HISTORY COPYRIGHT COMPILE
%{_bindir}/sq

%files -n %{libname}
%{_libdir}/libsqstdlib-%{version}.so
%{_libdir}/libsquirrel-%{version}.so

%files -n %{develname}
%{_includedir}/%{name}
%{_libdir}/libsqstdlib.so
%{_libdir}/libsquirrel.so
%{_libdir}/pkgconfig/*
