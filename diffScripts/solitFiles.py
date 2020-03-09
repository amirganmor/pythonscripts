from fsplit.filesplit import FileSplit
#1000000 = MG give or take
#fs = FileSplit(file='C:\\Users\\amir\\Desktop\\pyLib\\tmpDir\\zz\\affiliate_wp_visits_0.json', splitsize=5000000, output_dir='C:\\Users\\amir\\Desktop\\pyLib\\tmpDir\\zz\\out1\\')
s = FileSplit(file='C:\\Users\\amir\\Downloads\\lmntr_stream_meta_14\\lmntr_stream_meta_14.json', splitsize=60000000, output_dir='C:\\Users\\amir\\Downloads\\lmntr_stream_meta_14\\z\\')
s.split()
