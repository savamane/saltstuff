freight_repository:
  pkgrepo.managed:
    - humanname: freight
    - name: deb http://build.openvpn.net/debian/freight_team trusty main
    - file: /etc/apt/sources.list.d/freight.list
    - key_url: https://swupdate.openvpn.net/repos/repo-public.gpg

freight_package:
  pkg.latest:
    - pkgs:
      - freight
      - apache2

freight_config:
  file.managed:
    - name: /etc/freight.conf
    - source: salt://freight/files/etc/freight.conf.jinja
    - template: jinja

freight_gnupg_module:
  pip.installed:
    - name: gnupg
    - reload_modules: True

freight_gpg_key:
  file.managed:
    - name: /root/.gnupg/secret.gpg
    - makedirs: True
    - contents_pillar: freight:private-gpg
    - user: root
    - group: root
    - mode: 700
    - dir_mode: 700

freight_public_key:
  file.managed:
    - name: /var/www/freight/cache/pubkey.gpg
    - contents_pillar: freight:public-gpg

freight_import_key:
  cmd.run:
    - name: gpg --no-tty --allow-secret-key-import --import /root/.gnupg/secret.gpg
    - unless: gpg --no-tty --list-keys | grep {{ pillar['freight']['gpg-id'] }}
    - require:
      - file: freight_gpg_key

freight_apache_vhost:
  - file.managed:
    - name: /etc/apache2/sites-available/000-default.conf
    - source: salt://freight/files/etc/apache2/sites-available/000-default.conf

freight_apache_service:
  service.running:
    - name: apache2
    - enable: True
    - watch:
      - file: freight_apache_vhost

