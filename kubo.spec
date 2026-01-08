%define debug_package %{nil}

Name:     kubo
Version:  0.39.0
Release:  1
Summary:  IPFS implementation in Go
License:  MIT
Group:    Networking/Other
URL:      https://github.com/ipfs/%{name}
Source0:  https://github.com/ipfs/%{name}/releases/download/v%{version}/%{name}-source.tar.gz

BuildRequires:  golang

%description
IPFS is a global, versioned, peer-to-peer filesystem. It combines good ideas 
from Git, BitTorrent, Kademlia, SFS, and the Web. It is like a single bittorrent
swarm, exchanging git objects. kubo (previously go-ipfs) provides an interface 
as simple as the HTTP web, but with permanence built in. You can also mount the
world at /ipfs.

%prep
%autosetup -c -p 1

%build
# Set build environment, in particular use "-mod=vendor" to use the Go modules from the source archive's vendor dir
export BUILD_USER=abf BUILD_HOST=OpenMandriva
export CGO_CPPFLAGS="${CPPFLAGS}" CGO_CFLAGS="${CFLAGS}" CGO_CXXFLAGS="${CXXFLAGS}" CGO_LDFLAGS="${LDFLAGS}"
export GOFLAGS="-trimpath -buildvcs=false -buildmode=pie -mod=vendor"

go build -o ./cmd/ipfs/ipfs ./cmd/ipfs

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_userunitdir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

cp cmd/ipfs/ipfs %{buildroot}%{_bindir}

cat << EOF >>  %{buildroot}%{_userunitdir}/ipfs.service
[Unit]
Description=InterPlanetary File System (IPFS) daemon

[Service]
ExecStart=/usr/bin/ipfs daemon
Restart=on-failure

[Install]
WantedBy=default.target
EOF
cat << EOF >> %{buildroot}%{_unitdir}/ipfs@.service
[Unit]
Description=InterPlanetary File System (IPFS) daemon

[Service]
User=%i
ExecStart=/usr/bin/ipfs daemon
Restart=on-failure

[Install]
WantedBy=default.target
EOF

install -m 0644 docs/logo/%{name}-logo.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%files
%{_bindir}/ipfs
%{_userunitdir}/ipfs.service
%{_unitdir}/ipfs@.service
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%license LICENSE*
%doc docs/config.md
%doc docs/examples/example-folder
%doc docs/changelogs
%doc docs/production
%doc docs/specifications
