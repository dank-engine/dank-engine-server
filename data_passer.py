from google.transit import gtfs_realtime_pb2
import requests
import time

lines = ['BDBN', 'BDBR', 'BDRW', 'BDVL', 'BNBD', 'BNBR', 'BNDB', 'BNFG', 'BNSH', 'BRBD', 'BRBN', 'BRCA', 'BRCL', 'BRDB', 'BRFG', 'BRGY', 'BRIP', 'BRNA', 'BRRP', 'BRRW', 'BRSH', 'BRSP', 'BRVL', 'CABR', 'CACL', 'CAIP', 'CARW', 'CASP', 'CLBR', 'CLDB', 'CLSH', 'DBBN', 'DBBR', 'DBCL', 'DBDB', 'FGBN', 'FGBR', 'GYBR', 'IPBR', 'IPCA', 'IPDB', 'IPFG', 'IPNA', 'IPRP', 'IPRW', 'NABR', 'NAIP', 'NASP', 'RBUS', 'RPBR', 'RPCL', 'RPIP', 'RPSP', 'RWBD', 'RWBR', 'RWCA', 'RWIP', 'RWNA', 'RWRP', 'SHBN', 'SHBR', 'SHCL', 'SHSP', 'SPBR', 'SPCA', 'SPDB', 'SPNA', 'SPRP', 'VLBD', 'VLBR', 'VLDB']

def parse_train_data(input_data, chosen_lines):
    """
    Takes a list of lines and returns the data neccesary to interact with.

    Parameters:
        chosen_lines(list): List of Lines to get data for.

    Returns:
        [(route_id, trip_id, previous_stop_id, next_stop_id, stopped, Percentage_complete), ...]

    """
    data = []
    vehicle_data = []
    output = []   

    # Gather the Protobuffer
    feed = gtfs_realtime_pb2.FeedMessage()
    current_time = round(time.time())
    
    feed.ParseFromString(input_data)

    # Begin Stripping of Data
    message = feed.entity
    for entity in message:
        append = True
        if entity.trip_update.trip.HasField("schedule_relationship"):
            append = False
        elif entity.trip_update.trip.route_id[0:4] not in chosen_lines:
            append = False

        if not entity.HasField("trip_update") and entity.vehicle.trip.route_id[0:4] in chosen_lines:
            vehicle_data.append(entity)

        if append:
            data.append(entity)
        
    train_stopped = {}
    for entry in vehicle_data:
        trip_id = entry.vehicle.trip.trip_id

        current_status = entry.vehicle.current_status
        train_stopped[trip_id] = current_status



    for entry in data:
        stop_info = entry.trip_update.stop_time_update

        for index in range(len(stop_info)):
            if stop_info[index].arrival.time >= current_time:
                if index != 0:
                    prev_stop_id = stop_info[index-1].stop_id
                    next_stop_id = stop_info[index].stop_id
                    arrival_time = stop_info[index].arrival.time
                    departure_time = stop_info[index-1].departure.time
                    complete = (current_time-departure_time)/(arrival_time-departure_time)
                    if complete < 0:
                        complete = -2
                else:
                    complete = -1
                    prev_stop_id = -1
                    departure_time = -1
                    next_stop_id = stop_info[index].stop_id
                    arrival_time = stop_info[index].arrival.time
                break

                     
        trip_id = entry.trip_update.trip.trip_id
        route_id = entry.trip_update.trip.route_id

        stopped = train_stopped.get(trip_id)
        
        packet = (route_id, trip_id, prev_stop_id, next_stop_id, stopped, complete)
        if stopped:
            output.append(packet)

    return output