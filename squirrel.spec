%define _disable_ld_no_undefined %{nil}

%define oname %{name}%(echo %{version} | cut -d. -f1)

%define libname %mklibname %{name} %{version}
%define develname %mklibname %{name} -d

%define ver %(echo %{version} |sed -e 's,\\.,_,g')

Name:		squirrel
Version:	3.1
Release:	3
Summary:	The squirrel language
License:	zlib
Group:		Development/Other
URL:		http://squirrel-lang.org
Source0:	http://skylink.dl.sourceforge.net/project/squirrel/squirrel3/squirrel%20%{version}%20stable/squirrel_%{ver}_stable.tar.gz
Patch0:         squirrel-autoconfiscate.patch

%libpackage squirrel 0

%libpackage sqstdlib 0

%description
Squirrel is a light weight programming language 
featuring higher-order functions,classes/inheritance,
delegation,tail recursion,generators,cooperative 
threads,exception handling, reference counting and 
garbage collection on demand. C-like syntax.

%package -n %{develname}
Summary:	Header files and static libraries from %{name}
Group:		Development/Other
Requires:	%{mklibname squirrel 0} = %{EVRD}
Requires:	%{mklibname sqstdlib 0} = %{EVRD}
Provides:	lib%{name}-devel = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{mklibname %{name} 0 -d} < 3.1

%description -n %{develname}
Libraries and includes files for
developing programs based on %name.


%prep
%setup -qn %{oname}
%apply_patches

# fix file permissions
find . -type f -exec chmod a-x {} \;
chmod +x configure config.guess config.sub

# fix EOL + preserve timestamps
for f in README HISTORY COPYRIGHT
do
    perl -pi -e 's/\015$//' $f
done

aclocal
autoheader
automake -a
autoconf

%build
%global optflags %optflags -fPIC

%configure \
	--includedir=%{_includedir}/%{name}
%make

%install
%makeinstall_std INSTALL="/usr/bin/install -p"

# correct wrong file end of line encoding 
perl -pi -e 's/\015$//' %{buildroot}/%{_includedir}/*

# Add pkgconfig file
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cat >%{buildroot}%{_libdir}/pkgconfig/squirrel.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/squirrel

Name: %{name}
Description: squirrel library
Version: %{version}

Requires:
Libs: -L\${libdir} -lsquirrel -lsqstdlib
Cflags: -I\${includedir}
EOF

# Fix SUSE-ism
mv %{buildroot}%{_docdir}/packages/%{name} %{buildroot}%{_docdir}/%{name}
rmdir %{buildroot}%{_docdir}/packages

%files
%doc README HISTORY COPYRIGHT COMPILE
%{_bindir}/sq

%files -n %{develname}
%doc %{_datadir}/%{name}/examples
%{_includedir}/%{name}
%{_libdir}/libsqstdlib.so
%{_libdir}/libsquirrel.so
%{_libdir}/pkgconfig/*
