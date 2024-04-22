import os

# path_name = 'pomfred'
# i = 0
# for item in os.listdir(path_name):
#     os.rename(os.path.join(path_name, item), os.path.join(path_name, 'pomfred'+str(i)+'.png'))
#     i += 1


# path_name = 'silver carp'
# i = 0
# for item in os.listdir(path_name):
#     os.rename(os.path.join(path_name, item), os.path.join(path_name, 'silver_carp'+str(i)+'.png'))
#     i += 1

path_name = 'Pomfret'
i = 0
for item in os.listdir(path_name):
    os.rename(os.path.join(path_name, item), os.path.join(path_name, 'pomfret'+str(i)+'.png'))
    i += 1