#!/usr/bin/env bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

need_root() {
  if [[ ${EUID:-$(id -u)} -ne 0 ]]; then
    echo "Run as root or via sudo." >&2
    exit 1
  fi
}

have() {
  command -v "$1" >/dev/null 2>&1
}

apt_install() {
  apt-get update
  apt-get install -y \
    libarchive-tools \
    genisoimage \
    ssdeep \
    python3-ssdeep \
    python3-tlsh \
    radare2 \
    rizin \
    pesign \
    oletools \
    pdfid \
    pdf-parser \
    mono-devel \
    jadx \
    apktool
}

pipx_install() {
  local pkg="$1"
  if ! pipx list --short 2>/dev/null | awk '{print $1}' | grep -qx "$pkg"; then
    pipx install "$pkg"
  fi
}

setup_ghidra() {
  local ghidra_headless="/usr/share/ghidra/support/analyzeHeadless"
  local ghidra_wrapper_src="/tmp/sir/.ghidra-skill-src/mitsuhiko-agent-stuff/skills/ghidra/scripts/ghidra-analyze.sh"

  if [[ -x "$ghidra_headless" ]]; then
    ln -sf "$ghidra_headless" /usr/local/bin/analyzeHeadless
  fi

  if [[ -f "$ghidra_wrapper_src" ]]; then
    install -m 0755 "$ghidra_wrapper_src" /usr/local/bin/ghidra-analyze.sh
  elif [[ -x /usr/local/bin/analyzeHeadless ]]; then
    cat >/usr/local/bin/ghidra-analyze.sh <<'EOF'
#!/usr/bin/env bash
exec /usr/local/bin/analyzeHeadless "$@"
EOF
    chmod +x /usr/local/bin/ghidra-analyze.sh
  fi
}

main() {
  need_root

  if ! have apt-get; then
    echo "apt-get not found; this script is intended for Debian/Kali systems." >&2
    exit 1
  fi

  apt_install

  if ! have pipx; then
    apt-get install -y pipx
  fi

  pipx ensurepath >/dev/null 2>&1 || true
  pipx_install flare-capa
  pipx_install floss

  setup_ghidra

  echo "Installed/verified:"
  for cmd in file sha256sum strings objdump readelf exiftool jq curl 7z unzip timeout analyzeHeadless ghidra-analyze.sh capa floss ssdeep yara osslsigncode sigtool pdfid pdf-parser monodis jadx apktool; do
    if have "$cmd"; then
      printf '  %-18s %s\n' "$cmd" "$(command -v "$cmd")"
    else
      printf '  %-18s MISSING\n' "$cmd"
    fi
  done
}

main "$@"
