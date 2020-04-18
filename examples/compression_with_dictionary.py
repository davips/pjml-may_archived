import zstandard as zs
import os

samples = [os.urandom(30) for _ in range(500)]
size = 258
dict_data = zs.train_dictionary(
    dict_size=size, samples=samples, threads=-1
)
dic = False
if dic:
    cctx = zs.ZstdCompressor(threads=-1, dict_data=dict_data,
                             write_dict_id=False)
else:
    cctx = zs.ZstdCompressor(threads=-1, write_dict_id=False)

t=b'abcdefghijklmnopqrstuvwxyz'
print(len(t))

c = cctx.compress(t)
print(len(c), c)

cctx = zs.ZstdDecompressor(dict_data=dict_data)
print(cctx.decompress(c))

# TODO: round numbers in config to reduce total size when converted to string
