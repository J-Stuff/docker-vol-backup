import os
files = [f for f in os.listdir('.') if os.path.isfile(f)]

archive_parts = []

for f in files:
    if f.startswith("reassemble"):
        pass
    elif f.endswith(".zip.part0"):
        likely_name = f.split(".zip.part0")[0]
        break

for f in files:
    if f.startswith(likely_name):
        archive_parts.append(f)

with open(likely_name + ".zip", 'wb') as outfile: #type:ignore
    parts_length = len(archive_parts)
    print(f"Reassembling archive... ({parts_length} parts)")
    for i in range(parts_length):
        part_num = int(i)
        part = f"{likely_name}.zip.part{part_num}"
        print("Reassembling part: " + part)
        with open(part, 'rb') as infile:
            outfile.write(infile.read())
            print(f"Appended part {i} to {likely_name}")
    outfile.close()
