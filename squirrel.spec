%define oname SQUIRREL2

#there's no major in soname
%define libname		%mklibname %{name}
%define develname	%mklibname %{name} -d

Summary:	The squirrel language
Name:		squirrel
Version:	2.2.4
Release:	%mkrel 2
License:	GPLv2+
Group:		Development/Other
URL:		http://squirrel-lang.org
Source0:	http://ovh.dl.sourceforge.net/sourceforge/squirrel/%{name}_%{version}_stable.tar.bz2
Patch0:		squirrel_2.2.4_stable-autotools.patch
Conflicts:	ispell
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Squirrel is a light weight programming language 
featuring higher-order functions,classes/inheritance,
delegation,tail recursion,generators,cooperative 
threads,exception handling, reference counting and 
garbage collection on demand. C-like syntax.

%package -n %{libname}
Summary:	Shared libraries from %{name}
Group:		System/Libraries

%description -n %{libname}
Shared libraries from %{name}.

%package -n %{develname}
Summary:	Header files and static libraries from %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 0 -d

%description -n %{develname}
Development libraries and includes files for developing programs
based on %{name}.

%prep
%setup -q -n %{oname}
%patch0 -p1 -b .autotools

# fix file permissions
find . -type f -exec chmod a-x {} \;

# fix extension for autotools
mv sq/sq.c sq/sq.cpp

# fix EOL + preserve timestamps
for f in README HISTORY
do
    sed -i.orig 's/\r//g' $f
    touch -r $f.orig $f
done

%build
sh autogen.sh
%configure2_5x --disable-static
%make

%install
rm -rf %{buildroot}
%makeinstall_std

#we don't want these
rm -rf %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README HISTORY
%{_bindir}/sq

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libsqstdlib-%{version}.so
%{_libdir}/libsquirrel-%{version}.so

%files -n %{develname}
%defattr(-,root,root)
%doc doc/*.pdf
%{_libdir}/libsqstdlib.so
%{_libdir}/libsquirrel.so
%{_includedir}/squirrel
