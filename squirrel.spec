%define oname SQUIRREL2
%define packagedir SQUIRREL2

%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	The squirrel language
Name:		squirrel
Version:	2.2
Release:	%mkrel 2
License:	GPLv2+
Group:		Development/Other
URL:		http://squirrel-lang.org
Source:		http://ovh.dl.sourceforge.net/sourceforge/squirrel/%{name}_%{version}_stable.tar.bz2
Conflicts:	ispell
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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

%build

perl -pi -e 's/\015$//' HISTORY
perl -pi -e 's/\015$//' README
perl -pi -e 's/\015$//' COPYRIGHT
perl -pi -e 's/\015$//' doc/*

%install
install -d -m755 %{buildroot}/%{_bindir}
install -d -m755 %{buildroot}/%{_libdir}/%{name}
install -d -m755 %{buildroot}/%{_docdir}/%{name}
install -d -m755 %{buildroot}/%{_includedir}/%{name}

%ifnarch ix86
%make sq64
%else
%make
%endif

install  ../%{packagedir}/bin/sq %{buildroot}/%{_bindir}
install  ../%{packagedir}/lib/*.a %{buildroot}/%{_libdir}/%{name}
install  ../%{packagedir}/doc/*  %{buildroot}/%{_docdir}/%{name}
install  ../%{packagedir}/include/* %{buildroot}/%{_includedir}

#correct wrong file end of line encoding 
perl -pi -e 's/\015$//' %{buildroot}/%{_includedir}/*

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}
%attr(755,root,root) %{_bindir}/sq

%files -n %{develname}
%defattr(644,root,root,755)
%{_includedir}/sq*.h
%{_libdir}/%{name}/*
