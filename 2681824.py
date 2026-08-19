import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--data-file",
    type=str,
    default="Data/easy.txt",
    help="Process data input into the student and marker file",
)

args = parser.parse_args()

processes = []
started = 0
counter = []
io_counter = []

def pop_from_io_counter(el):
    for idx, x in enumerate(io_counter):
        if el["ID"] == x["ID"]:
            io_counter.pop(idx)

def pop_from_counter(el):
    for idx, x in enumerate(counter):
        if el["ID"] == x["ID"]:
            counter.pop(idx)

def start_processes(step, no_processes, started):
    for i in range(started, no_processes):
        if processes[i]["At"] <= step:
            counter.append(processes[i])
            if processes[i]["IO"] > 0:
                io_counter.append(processes[i])
            started += 1
            continue
        else:
            break
    counter.sort(key=lambda process: process["Tt"] - process["St"])
    io_counter.sort(key=lambda process: process["IOCounter"])
    return started

def process(schedule, counter_idx, obj):
    if counter[counter_idx]["Rt"] - counter[counter_idx]["St"] > 0:
        schedule.append(counter[counter_idx]["ID"])
        counter[counter_idx]["St"] += 1
    if counter[counter_idx]["IOCounter"] > 0:
        counter[counter_idx]["IOCounter"] -= 1
    if counter[counter_idx]["St"] == counter[counter_idx]["Rt"]:
        pop_from_io_counter(counter[counter_idx])
        counter.pop(counter_idx)
        return 1
    return 0

def schedule_processes():
    global started
    no_processes = len(processes)
    ended = 0
    step = 0
    schedule = []
    while ended != no_processes:
        # print(step, ended, no_processes, started, counter)
        started = start_processes(step, no_processes, started)
        if len(io_counter) > 0 and io_counter[0]["IOCounter"] == 0:
            schedule.append("!" + io_counter[0]["ID"])
            io_counter[0]["IOCounter"] = io_counter[0]["IO"]
            for idx, x in enumerate(counter):
                if io_counter[0]["ID"] == x["ID"]:
                    continue
                ended += process(schedule, idx, x)
            io_counter.sort(key=lambda process: process["IOCounter"])
        elif len(counter) > 0:
            ended += process(schedule, 0, counter[0])
        step += 1
    return step, schedule

def main():
    # Open the file for reading
    try:
        with open(args.data_file, "r") as file:
            data = file.read()
    except FileNotFoundError:
        return 1

    """
    TODO: Your scheduling algorithm here.
    Assign your result to the output variable.
    """
    for x in data.split("\n"):
        process = x.split(",")
        if len(process) == 1:
            continue
        obj = {
            "ID": process[0],
            "Rt": int(process[1]),
            "At": int(process[2]),
            "Tt": int(process[1]) + int(process[3]),
            "IO": int(process[3]),
            "IOCounter": int(process[3]),
            "St": 0,
        }
        processes.append(obj)
    processes.sort(key=lambda process: process["At"])

    steps, schedule = schedule_processes()

    return " ".join(schedule)

if __name__ == "__main__":
    scheduler_out = main()
    print(scheduler_out)
