%define sname mbed
%define oldname polarssl

%define major	9	
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d

%define oldlibname	%mklibname %{name} %{major}
%define olddevname	%mklibname %{name} -d

Summary:	An SSL library
Name:		%{sname}tls
Version:	2.4.0
Release:	0
License:	GPLv2+
Group:		System/Libraries
Url:		https://tls.mbed.org
Source0:	https://tls.mbed.org/code/releases/%{name}-%{version}-gpl.tgz

BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	perl
BuildRequires:	graphviz
BuildRequires:	pkgconfig(libpkcs11-helper-1)
BuildRequires:	pkgconfig(zlib)

Provides:	%{sname} = %{EVRD}
Provides:	%{oldname} = %{EVRD}

%description
%{name} TLS (formerly known as PolarSSL) makes it trivially easy for developers
to include cryptographic and SSL/TLS capabilities in their (embedded) products,
facilitating this functionality with a minimal coding footprint.

This package contains mbed TLS programs.

%files
%{_bindir}/*
%doc README.md
%doc ChangeLog
%doc gpl-2.0.txt
%doc LICENSE


#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	mbed TLS library
Group:		System/Libraries

Provides:	%{oldlibname} = %{EVRD}

%description -n %{libname}
mbed TLS (formerly known as PolarSSL) makes it trivially easy for developers
to include cryptographic and SSL/TLS capabilities in their (embedded) products,
facilitating this functionality with a minimal coding footprint.

This package contains the library itself.

%files -n %{libname}
%{_libdir}/lib%{sname}crypto.so.*
%{_libdir}/lib%{sname}tls.so.*
%{_libdir}/lib%{sname}x509.so.*
%doc gpl-2.0.txt
%doc LICENSE

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	mbed TLS development files
Group:		Development/C
Requires:	%{libname} = %{EVRD}

Provides:	%{name}-devel = %{EVRD}
Provides:	%{sname}-devel = %{EVRD}
Provides:	%{olddevname} = %{EVRD}

%description -n %{devname}
mbed TLS (formerly known as PolarSSL) makes it trivially easy for developers
to include cryptographic and SSL/TLS capabilities in their (embedded) products,
facilitating this functionality with a minimal coding footprint.

This package contains development files.

%files -n %{devname}
%{_includedir}/%{name}/
%{_libdir}/lib%{sname}crypto.so
%{_libdir}/lib%{sname}tls.so
%{_libdir}/lib%{sname}x509.so
%doc apidoc
%doc gpl-2.0.txt
%doc LICENSE

#----------------------------------------------------------------------------

%prep
%setup -q

enable_mbedtls_option() {
    local myopt="$@"
    # check that config.h syntax is the same at version bump
    sed -i \
        -e "s://#define ${myopt}:#define ${myopt}:" \
        include/mbedtls/config.h || die
}

enable_mbedtls_option MBEDTLS_ZLIB_SUPPORT
enable_mbedtls_option MBEDTLS_HAVEGE_C

%build
%cmake \
	-DCMAKE_BUILD_TYPE:STRING="Release" \
	-DUSE_SHARED_MBEDTLS_LIBRARY:BOOL=ON \
	-DUSE_STATIC_MBEDTLS_LIBRARY:BOOL=OFF \
	-DENABLE_PROGRAMS:BOOL=ON \
	-DENABLE_TESTING:BOOL=ON \
	-DENABLE_ZLIB_SUPPORT:BOOL=ON \
	-DUSE_PKCS11_HELPER_LIBRARY:BOOL=ON \
	-DLINK_WITH_PTHREAD:BOOL=ON
%make all

# doc
%make apidoc

%install
%makeinstall_std -C build

# fix file name
mv %{buildroot}%{_bindir}/benchmark %{buildroot}%{_bindir}/benchmark.%{name}

%check
# tests
LD_LIBRARY_PATH=%{buildroot}%{_libdir} %make -C build test

