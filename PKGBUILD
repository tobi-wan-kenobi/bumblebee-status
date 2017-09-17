# Maintainer: Tobias Witek <tobi@tobi-wan-kenobi.at>
# Contributor: Daniel M. Capella <polycitizen@gmail.com>

pkgname=bumblebee-status
pkgver=1.4.2
pkgrel=1
pkgdesc='Modular, theme-able status line generator for the i3 window manager'
arch=('any')
url=https://github.com/tobi-wan-kenobi/bumblebee-status
license=('MIT')
depends=('python' 'python-netifaces' 'python-psutil' 'python-requests')
optdepends=('xorg-xbacklight: to display a displays brightness'
            'xorg-xset: enable/disable automatic screen locking'
            'libnotify: enable/disable automatic screen locking'
            'dnf: display DNF package update information'
            'xorg-setxkbmap: display/change the current keyboard layout'
            'redshift: display the redshifts current color'
            'pulseaudio: control pulseaudio sink/sources'
            'xorg-xrandr: enable/disable screen outputs'
            'pacman: display current status of pacman'
            'iputils: display a ping'
            'i3ipc-python: display titlebar'
            'fakeroot: dependency of the pacman module')
source=("$pkgname-$pkgver.tar.gz::$url/archive/v$pkgver.tar.gz")
sha512sums=('3a66fc469dd3b081337c9e213a1b2262f25f30977ee6ef65b9fa5a8b6aa341637832d1a5dbb74e30d68e2824e0d19d7a911eb3390dc6062707a552f429b483e8')

package() {
  install -d "$pkgdir"/usr/bin \
    "$pkgdir"/usr/share/$pkgname/{bumblebee/modules,themes/icons}
  ln -s /usr/share/$pkgname/$pkgname "$pkgdir"/usr/bin/$pkgname

  cd $pkgname-$pkgver
  cp -a --parents $pkgname bumblebee/{,modules/}*.py themes/{,icons/}*.json \
    "$pkgdir"/usr/share/$pkgname

  install -Dm644 LICENSE "$pkgdir"/usr/share/licenses/$pkgname/LICENSE
}
