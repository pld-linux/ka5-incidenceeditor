#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	23.04.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		incidenceeditor
Summary:	Incidence editor
Name:		ka5-%{kaname}
Version:	23.04.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	e902ba2ec1c5878621557a50f193f961
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= 5.11.1
BuildRequires:	Qt5Widgets-devel
BuildRequires:	cmake >= 2.8.12
BuildRequires:	gettext-devel
BuildRequires:	ka5-akonadi-devel >= %{kdeappsver}
BuildRequires:	ka5-akonadi-mime-devel >= %{kdeappsver}
BuildRequires:	ka5-calendarsupport-devel >= %{kdeappsver}
BuildRequires:	ka5-eventviews-devel >= %{kdeappsver}
BuildRequires:	ka5-kcalutils-devel >= %{kdeappsver}
BuildRequires:	ka5-kldap-devel >= %{kdeappsver}
BuildRequires:	ka5-kmailtransport-devel >= %{kdeappsver}
BuildRequires:	ka5-kmime-devel >= %{kdeappsver}
BuildRequires:	ka5-libkdepim-devel >= %{kdeappsver}
BuildRequires:	kdiagram-devel >= 1.4.0
BuildRequires:	kf5-extra-cmake-modules >= %{kframever}
BuildRequires:	kf5-kcalendarcore-devel >= %{kframever}
BuildRequires:	kf5-kcodecs-devel >= %{kframever}
BuildRequires:	kf5-ki18n-devel >= %{kframever}
BuildRequires:	kf5-kiconthemes-devel >= %{kframever}
BuildRequires:	kf5-kio-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This lib provides incidence editor.

%description -l pl.UTF-8
Ta biblioteka zawiera edytor listy rzeczy do zrobienia.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
install -d build
cd build
%cmake \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%ninja_build

%if %{with tests}
ctest
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%{_datadir}/qlogging-categories5/incidenceeditor.categories
%{_datadir}/qlogging-categories5/incidenceeditor.renamecategories
%ghost %{_libdir}/libKPim5IncidenceEditor.so.5
%attr(755,root,root) %{_libdir}/libKPim5IncidenceEditor.so.*.*.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/qt5/mkspecs/modules/qt_IncidenceEditor.pri
%{_includedir}/KPim5/IncidenceEditor
%{_libdir}/cmake/KF5IncidenceEditor
%{_libdir}/cmake/KPim5IncidenceEditor
%{_libdir}/libKPim5IncidenceEditor.so

