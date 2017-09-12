while true

do
  ./adb.exe shell input tap 1400 1300
  sleep 1
  ./adb.exe shell input tap 2300 400
  sleep 1
  # ./adb.exe shell input tap 1300 1580
  # sleep 1
done
