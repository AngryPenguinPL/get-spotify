%define tmp_download_dir %{_localstatedir}/lib/%{oname}

%define oname spotify

Summary:	Download and Install Spotify client for OpenMandriva
Name:		get-%{oname}
Version:	1.0.92.390
Release:	1
License:	Proprietary
Group:		Networking/WWW
Url:		https://www.spotify.com/pl/download/linux/
Requires:	wget
Requires: dpkg
ExclusiveArch:	x86_64
#Conflicts:	spotify = beta

%description
This is an installer for Spotify for Linux OpenMandriva.

This package does not contain any program files from Spotify. By installing this package you will download and
install Spotify from official Spotify Debian repository. OpenMandriva not hosing or redistribute any files.
By using this, you accept the Spotify EULA.
Please be patient, this is about 100 MB download and may take some time.
Removing this package will uninstall Spotify from your system.

%files

%pre
mkdir -p %{tmp_download_dir}
[[ -d %{tmp_download_dir} ]] || exit 1
cd %{tmp_download_dir} || exit 1

#wget --force-clobber --timeout=30 --tries=3 "https://repo.yandex.ru/yandex-browser/rpm/beta/x86_64/%{oname}-beta-%{version}-1.x86_64.rpm"
wget --force-clobber --timeout=30 --tries=3 "http://repository.spotify.com/pool/non-free/s/%{oname}-client/spotify-client_%{version}.g2ce5ec7d-18_amd64.deb

%post
tmp_extract_dir=$(mktemp -d)
if ! [[ -d $tmp_extract_dir ]]; then
echo "Failed to create temporary directory"
rm -r %{tmp_download_dir}
exit 1
fi

# Spotify from company Spotify AB
#if [ `rpm -q %{oname}-beta | wc -w` == 1 ]
#then
#	rpm -e %{oname}-beta
#fi
#
# Old version
#if [ `rpm -q %{name} | wc -w` == 1 ]
#then
#	rpm -e %{name}
#fi

%define tmp_yb_dir ${tmp_extract_dir}/%{oname}-%{version}

mkdir -p %{tmp_yb_dir}
cd %{tmp_yb_dir}
dpkg -x "%{tmp_download_dir}/spotify-client_%{version}.g2ce5ec7d-18_amd64.deb %{tmp_yb_dir}

#if ! [[ -d %{tmp_yb_dir} ]]; then
#echo "Extracted file folder missing"
#cd ..
#rm -rf ${tmp_extract_dir}
#rm -r %{tmp_download_dir}
#exit 1
#fi

cp -rf %{tmp_yb_dir}%{_datadir}/ %{_datadir}
#cp -rf %{tmp_yb_dir}%{_sysconfdir}/ %{_sysconfdir}/
mv -f %{tmp_yb_dir}%{_bindir}/%{oname} %{_bindir}/%{oname}
mv -f %{tmp_yb_dir}%{_datadir}/%{oname}/%{oname}.desktop %{_datadir}/applications/%{oname}.desktop
mkdir -p /usr/share/spotify/
cp -rf %{tmp_yb_dir}/spotify/usr/share/spotify/* /usr/share/spotify/

cd ..
rm -r ${tmp_extract_dir} %{tmp_download_dir}
echo "Done!"

# Remove spotify-install package if we have it installed
#if [ `rpm -q %{oname}-install | wc -w` == 1 ]
#then
#	rpm -e %{oname}-install
#fi

#preun
#rm -f %{_bindir}/%{oname}
#rm -f %{_bindir}/appdata/yandex-browser-beta.appdata.xml
#rm -f %{_bindir}/applications/yandex-browser-beta.desktop
#rm -f %{_bindir}/gnome-control-center/default-apps/yandex-browser-beta.xml
#rm -f %{_datadir}/applications/%{oname}-beta.desktop
#rm -f %{_mandir}/man1/yandex-browser-beta.1.gz
#rm -rf opt/yandex/browser-beta

#----------------------------------------------------------------------------

%prep

%build

%install
