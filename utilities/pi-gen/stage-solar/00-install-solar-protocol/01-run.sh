on_chroot <<EOF
git clone https://github.com/alexnathanson/solar-protocol --depth 1 /home/pi/solar-protocol
a2enmod headers
a2enmod rewrite
a2enmod userdir
a2enmod ssl
adduser pi www-data
chown -R pi:pi /home/pi/solar-protocol
chown -R www-data:www-data /home/pi/solar-protocol/frontend
chmod 755 /home/pi
EOF

sed \
  -e 's|\[sshd\]|\[sshd\]\n\nenabled = true\nfilter = sshd|' \
  ${ROOTFS_DIR}/etc/fail2ban/jail.conf > ${ROOTFS_DIR}/etc/fail2ban/jail.local

# TODO: confirm with Alex if this is safe to remove
#sed -i \
#  -e 's|;date.timezone.*|date.timezone = ${{ steps.config.outputs.timezone_default }}|' \
#  ${ROOTFS_DIR}/etc/php/8.2/apache2/php.ini

echo 'PubkeyAcceptedAlgorithms +ssh-rsa' >> ${ROOTFS_DIR}/etc/ssh/sshd_config

sed -i \
  -e 's|DocumentRoot /var/www/html|DocumentRoot /home/pi/solar-protocol/frontend|' \
  -e 's|</VirtualHost>|\t<Location /server-status>\n\t\tSetHandler server-status\n\t\tRequire all granted\n\t</Location>\n</VirtualHost>|' \
  -e 's|*:80>|*:8080>|' \
  ${ROOTFS_DIR}/etc/apache2/sites-available/000-default.conf

echo 'Listen 8080' >> ${ROOTFS_DIR}/etc/apache2/ports.conf

cat >> ${ROOTFS_DIR}/etc/apache2/apache2.conf <<EOF

<Directory /home/pi/solar-protocol/frontend/>
    Options Indexes FollowSymLinks
    AllowOverride All
    Require all granted
    Header set Access-Control-Allow-Origin
</Directory>
EOF

rm ${ROOTFS_DIR}/etc/motd
rm ${ROOTFS_DIR}/etc/update-motd.d/10-uname
envsubst < files/10-hello.template > ${ROOTFS_DIR}/etc/update-motd.d/10-hello
chmod a+x ${ROOTFS_DIR}/etc/update-motd.d/10-hello
envsubst < files/20-warning.template > ${ROOTFS_DIR}/etc/update-motd.d/20-warning
chmod a+x ${ROOTFS_DIR}/etc/update-motd.d/20-warning

on_chroot << EOF
  pushd /home/pi/solar-protocol
  python -m venv .venv
  . .venv/bin/activate
  python -m pip install -r requirements.txt
  cp -r local ../
  cp backend/data/deviceListTemplate.json backend/data/deviceList.json
  chown -R pi:pi /home/pi
EOF
