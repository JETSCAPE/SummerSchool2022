curlcmd=wget
command -v ${curlcmd} > /dev/null || curlcmd="curl -LO"
command -v ${curlcmd} > /dev/null || { echo "Please install curl or wget" ; exit 1; }
$curlcmd "http://yasuki.sakura.ne.jp/JETSCAPE_HYDRO_PROFILE/test_hydro_profile.tar.gz"

tar xvzf test_hydro_profile.tar.gz
