mesosphere_repos-gpgkey:
  file.managed:
    - name: /etc/pki/rpm-gpg/RPM-GPG-KEY-mesosphere
    - contents: |
        -----BEGIN PGP PUBLIC KEY BLOCK-----
        Version: GnuPG v1.4.14 (GNU/Linux)

        mQINBFN9MbMBEADQ12KLwGs5zfhuek+rJKFlhKzqwfJj6EGEIID7kCp0ev5dV+xr
        T9jIT+BBjT36WW+49gPDcHCsL+d3oQQxn2wiNyQ+Di+vgCEjPG9pUwgWjX57Ug7l
        MMNziIrSI48WwNqBCANf438q6qiqOZKPrh5xz4NlbxfCuLnt7xhh5ypmi12A+t1+
        l1WqQr0/Wmor1t0FxmXkx5le+tkhTKpl0Man4y3XK4/5zwbUYOMHJtoLbYg+4pQQ
        yu3fRyyzYSxpl2GyoLh4ksB6kQD6tU0X/9FQIH0nIFIUa9oLeDwtFM9h0/oIN/3C
        vDFwCY+cxYZUNoHUTURwPFR/exIb34yYYRsuLHIeo1PV8J+KQBLv8WYtuFvC4Upx
        qjq0+i1EtRvc8/xLsJJoVrQebMHioeMjMdAla+A/zAiJNo2As7a6XaFZd2S4ra+t
        ZhvFXr1jR6pvSS4vFhdn7BJ2JOqzGDmBEttQO4Qer4mQavKwSgp9H8h/SV9AHXEZ
        uRKIBtutV/wJoQF7dEcnQCw4RKPLyqOxc9+bRkhd/3fyH5XEhiJJPv4KsY8yi2+X
        cYCOkJLgtTLtgqil9YMDqDkVl+Lossp81/xQmpFgT4R8KPBlQP5OL+J0q0kpmBs+
        gS5PCa2bj8Eb9nBz6j2q3VtpbcDtIgGtIuHfe+HedZ+0g3cWm10MnslflQARAQAB
        tEBNZXNvc3BoZXJlIEFyY2hpdmUgQXV0b21hdGljIFNpZ25pbmcgS2V5IDxzdXBw
        b3J0QG1lc29zcGhlcmUuaW8+iQI3BBMBCgAhBQJTfTGzAhsDBQsJCAcDBRUKCQgL
        BRYDAgEAAh4BAheAAAoJEN99VMvlYVG/yXEP/AzeFA/3xs1i5ZcQpy+pzSA3yu3+
        lJCDjFr1IUiBjUr6OgQ+jmvRkGzZo2W4pi5mlkJIOTeVQ8MC+dYjvvPuZd6Ah4E1
        seAdJCM9md2KM0ez2cFzdsStQU2omI0LNwT/RVIXUrAYgTf0toaiK136DpkfSDqE
        on5XD8+8KA04sMdvvtQV6ZGL9gPP3Y/WQOEfRbNFjh+uacPkg2eA3CDIkfL+daS4
        7mOnD1Y6dle9TDdy3udNCO6klSoMF6ZvFm/RgjnK2NO6VTIg0sUiSNHCVwFhYgVF
        a3fgcAV5yL+DHDszV76fQOVg2QTKM+NIkReg/3LNQLdrx/JrrieGYfRdyNqNz3C+
        PTTDSIYLo9q3BjMWtsBofT8iA9YUK77Dihcnq3j9P4As49VPh/63srRrDDlM9Kt8
        nxmdsoO3q2vOllQJp2ZpFcOyvtz6bNWQ9/4uZLF3KrAMx36GZe4a9dTct/zIzi4D
        47XyEnD3jQlgXO0ue1i7LVRLWdjOVpSa2c/2VcmRBY+vIbr6V1HW97uQgsWSrmLp
        o3e/RfVLNnvKjFrbp+uOA3JegVbru6LLg1AU6LicipXBtFW0yey0LmB0BtjUm7GP
        GpxNJDw2FrTBv0Dem9iDVQEndelIcSDxGnNicBInZqjvzFDii2vfPTrwHSf8wnRD
        BCVhbLcsbiRBTIQR
        =zlOT
        -----END PGP PUBLIC KEY BLOCK-----
    - user: root
    - group: root
    - mode: 644

mesosphere_repos-arch:
  pkgrepo.managed:
    - name: mesosphere
    - humanname: Mesosphere Packages - $basearch
    - baseurl: http://repos.mesosphere.io/el/$releasever/$basearch/
    - enabled: 1
    - gpgcheck: 1
    - gpgkey: 'file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mesosphere'

mesosphere_repos-noarch:
  pkgrepo.managed:
    - name: mesosphere-noarch
    - humanname: Mesosphere Packages - noarch
    - baseurl: http://repos.mesosphere.io/el/$releasever/noarch/
    - enabled: 1
    - gpgcheck: 1
    - gpgkey: 'file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mesosphere'
