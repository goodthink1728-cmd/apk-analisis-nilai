[app]
title = Analisis Nilai
package.name = analisisnilai
package.domain = org.sekolah

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.api = 33
android.minapi = 21

[buildozer]
log_level = 2
warn_on_root = 1