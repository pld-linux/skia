#
# Conditional build:
%bcond_with	static_libs	# don't build static library
%bcond_without	verbose			# verbose build (V=1)

%define		subver	20130302
%define		rel		0.1
Summary:	2D graphic library
Name:		skia
Version:	0
Release:	0.%{rel}.%{subver}
License:	BSD
Group:		Development/Libraries
Source0:	%{name}-%{subver}.tar.xz
# Source0-md5:	e2de2d4871a315cd1e252f77cd96dca2
Source1:	get-source.sh
Source2:	gclient.conf
Patch0:		shared-libs.patch
URL:		https://sites.google.com/site/skiadocs/
BuildRequires:	Mesa-libGL-devel
BuildRequires:	Mesa-libGLU-devel
BuildRequires:	cityhash-devel >= 1.1.0
BuildRequires:	freetype-devel
BuildRequires:	libstdc++-devel
BuildRequires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Skia is a complete 2D graphic library for drawing Text, Geometries,
and Images.

%package devel
Summary:	The development files for skia
Summary(pl.UTF-8):	Pliki programistyczne skia
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for development with skia.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia programów z użyciem skia.

%package static
Summary:	Static skia library
Summary(pl.UTF-8):	Statyczna biblioteka skia
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static skia library.

%description static -l pl.UTF-8
Statyczna biblioteka skia.

%prep
%setup -qn %{name}-%{subver}
%patch0 -p1

%build
%{__python} gyp_skia \
	--format=make \
	--depth=. \
	skia.gyp

%{__make} -r \
	BUILDTYPE=%{!?debug:Release}%{?debug:Debug} \
	%{?with_verbose:V=1} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	LDFLAGS="%{rpmldflags} -fuse-ld=gold" \
	CC.host="%{__cc}" \
	CXX.host="%{__cxx}" \
	LDFLAGS.host="%{rpmldflags}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	CXXFLAGS="%{rpmcxxflags} %{rpmcppflags}" \
	skia_base_libs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/%{name}}

cp -a include/* $RPM_BUILD_ROOT%{_includedir}/%{name}

cd out/%{!?debug:Release}%{?debug:Debug}

install -p lib.target/lib*.so $RPM_BUILD_ROOT%{_libdir}

%if %{with static_libs}
cp -p lib*.a $RPM_BUILD_ROOT%{_libdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

# ldconfig to update ld.so.cache
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README LICENSE
%attr(755,root,root) %{_libdir}/libskia_core.so
%attr(755,root,root) %{_libdir}/libskia_gr.so
%attr(755,root,root) %{_libdir}/libskia_opts.so
%attr(755,root,root) %{_libdir}/libskia_opts_ssse3.so
%attr(755,root,root) %{_libdir}/libskia_ports.so
%attr(755,root,root) %{_libdir}/libskia_sfnt.so
%attr(755,root,root) %{_libdir}/libskia_skgr.so
%attr(755,root,root) %{_libdir}/libskia_utils.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libskia_core.a
%{_libdir}/libskia_gr.a
%{_libdir}/libskia_opts.a
%{_libdir}/libskia_opts_ssse3.a
%{_libdir}/libskia_ports.a
%{_libdir}/libskia_sfnt.a
%{_libdir}/libskia_skgr.a
%{_libdir}/libskia_utils.a
%endif
