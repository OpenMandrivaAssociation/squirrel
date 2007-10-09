%define  name squirrel 
%define  version 2.1.2
%define  release %mkrel 1
%define  summary The squirrel language
%define  aname SQUIRREL2
%define packagedir SQUIRREL2

%define major 0
%define libname %mklibname %name %major


Name:    %name
Version: %version
Release: %release
Summary: %summary
License: GPL
URL:    http://sourceforge.net/projects/squirrel/
Group:   Development/Other
Source:  http://ovh.dl.sourceforge.net/sourceforge/squirrel/%{name}_%{version}_stable.tar.bz2
Patch0:  %name.h.patch
BuildRoot: %{_tmppath}/%{name}-buildroot

Conflicts: ispell

%description
Squirrel is a light weight programming language 
featuring higher-order functions,classes/inheritance,
delegation,tail recursion,generators,cooperative 
threads,exception handling, reference counting and 
garbage collection on demand. C-like syntax.


%package -n     %{libname}-devel
Summary:        Header files and static libraries from %name
Group:          Development/Other
Provides:       lib%{name}-devel = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:      %name-devel


%description -n %{libname}-devel
Libraries and includes files for
developing programs based on %name.

%prep
rm -rf %buildroot

%setup -q -n %aname
%ifarch amd64
%patch0 -p0
%endif


%build

perl -pi -e 's/\015$//' HISTORY
perl -pi -e 's/\015$//' README
perl -pi -e 's/\015$//' COPYRIGHT
perl -pi -e 's/\015$//' doc/*

%install
install -d -m755 %buildroot/%_bindir
install -d -m755 %buildroot/%_libdir/%name
install -d -m755 %buildroot/%_docdir
install -d -m755 %buildroot/%_includedir/%name


make

install -m755 ../%{packagedir}/bin/sq %buildroot/%_bindir
install -m755 ../%{packagedir}/lib/*.a %buildroot/%_libdir/%name
install -m755 ../%{packagedir}/doc/*  %buildroot/%_docdir
install -m755 ../%{packagedir}/include/* %buildroot/%_includedir

#correct wrong file end of line encoding 
perl -pi -e 's/\015$//' %buildroot/%_includedir/* 


%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
%doc README COPYRIGHT HISTORY
%_bindir/sq
%_docdir/sq*.*

%files -n %{libname}-devel
%defattr(-,root,root)
%_includedir/sq*.h
%_libdir/%name/*


