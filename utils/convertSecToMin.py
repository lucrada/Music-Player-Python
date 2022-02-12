def convertSecToMin(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return '%02d:%02d' % (minutes, seconds)