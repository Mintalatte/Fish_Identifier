import os

path_name = 'Tincaeus'
i = 0
for item in os.listdir(path_name):
    os.rename(os.path.join(path_name, item), os.path.join(path_name, 'tincaeus'+str(i)+'.png'))
    i += 1


# path_name = 'SilverCarp'
# i = 0
# for item in os.listdir(path_name):
#     os.rename(os.path.join(path_name, item), os.path.join(path_name, 'silver_carp'+str(i)+'.png'))
#     i += 1

# path_name = 'Pomfret'
# i = 0
# for item in os.listdir(path_name):
#     os.rename(os.path.join(path_name, item), os.path.join(path_name, 'pomfret'+str(i)+'.png'))
#     i += 1