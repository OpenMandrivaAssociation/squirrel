%define _disable_ld_no_undefined %{nil}

%define oname SQUIRREL2
%define packagedir SQUIRREL2

%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Name:		squirrel
Version:	2.2.5
Release:	%mkrel 1
Summary:	The squirrel language
License:	zlib
Group:		Development/Other
URL:		http://squirrel-lang.org
Source0:	http://ovh.dl.sourceforge.net/sourceforge/squirrel/%{name}_%{version}_stable.tar.gz
Patch0:         %{name}-2.2.5-fdr-autotools.patch
Patch1:         %{name}-2.2.4-fdr-mem.patch
Patch2:		squirrel-automake-1.13.patch

%description
Squirrel is a light weight programming language 
featuring higher-order functions,classes/inheritance,
delegation,tail recursion,generators,cooperative 
threads,exception handling, reference counting and 
garbage collection on demand. C-like syntax.


%package -n %{develname}
Summary:	Header files and static libraries from %{name}
Group:		Development/Other
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

sh autogen.sh

%build
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

%files -n %{develname}
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*


%changelog

* Mon Feb 27 2012 kamil <kamil> 2.2.5-1.mga2
+ Revision: 215542
- new version 2.2.5
- sync .spec with Fedora
  o add patches:
  * P0 autotools.patch
  * P1 mem.patch
  o disable static library
- update license (it's zlib not GPL)

* Fri Apr 01 2011 dams <dams> 2.2.4-1.mga1
+ Revision: 79375
- imported package squirrel

