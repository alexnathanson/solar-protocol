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

cat > ${ROOTFS_DIR}/etc/fail2ban/jail.local <<EOF
[sshd]
enabled = true
filter = sshd
backend = systemd
logpath = /var/log/auth.log
maxretry = 5
bantime = 3600
EOF

# this is needed to make sure php has the correct timezone
sed -i \
  -e "s|;date.timezone.*|date.timezone = ${TIMEZONE_DEFAULT}|" \
  ${ROOTFS_DIR}/etc/php/8.2/apache2/php.ini

# TODO: check if needed or install to @reboot cron
# sh /home/pi/solar-protocol/utilities/setAllPermissions.sh

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
    Header set Access-Control-Allow-Origin "*"
</Directory>
EOF

export VERSION
rm ${ROOTFS_DIR}/etc/motd
rm ${ROOTFS_DIR}/etc/update-motd.d/10-uname
envsubst < files/etc/update-motd.d/10-hello.template > ${ROOTFS_DIR}/etc/update-motd.d/10-hello
chmod a+x ${ROOTFS_DIR}/etc/update-motd.d/10-hello

rm ${ROOTFS_DIR}/etc/issue
envsubst < files/etc/issue.template > ${ROOTFS_DIR}/etc/issue

install -d "${ROOTFS_DIR}/etc/systemd/system"
install -m 644 files/etc/systemd/system/userpass.service "${ROOTFS_DIR}/etc/systemd/system/userpass.service"
install -d "${ROOTFS_DIR}/usr/lib/userpass-pi"
install -m 755 files/usr/lib/userpass-pi/userpass-service "${ROOTFS_DIR}/usr/lib/userpass-pi/userpass-service"

on_chroot << EOF
  systemctl enable userpass.service
EOF

install files/home/pi/disable-ssh-password-auth "${ROOTFS_DIR}/home/pi/"

on_chroot << EOF
  pushd /home/pi/solar-protocol
  python -m venv .venv
  . .venv/bin/activate
  python -m pip install -r requirements.txt
  cp -r local ../
  cp utilities/build/installation.md /home/pi/readme.md
  cp backend/data/deviceListTemplate.json backend/data/deviceList.json
  chown -R pi:pi /home/pi
EOF
