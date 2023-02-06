
import argparse
import json
import os
import sys

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

field_mapping = {
    'windows|alert|intrusion_detection,malware|allowed,info|rule_detection': [],
    'windows|event|authentication,session|end|log_off': ['user_admin_logoff', 'user_explicit_logoff', 'user_logoff'],
    'windows|event|authentication,session|start|log_on': ['user_admin_logon', 'user_explicit_logon', 'user_logon', 'user_logon_failed'],
    'windows|event|driver|start|load': [],
    'windows|event|file|access|open': [],
    'windows|event|file|change|modification': [],
    'windows|event|file|change|overwrite': [],
    'windows|event|file|change|rename': [],
    'windows|event|file|creation|creation': [],
    'windows|event|file|deletion|deletion': [],
    'windows|event|library|start|load': [],
    'windows|event|network|end|disconnect_received': ['ipv4_disconnect_received', 'ipv6_disconnect_received'],
    'windows|event|network|info,protocol|lookup_requested': [],
    'windows|event|network|info,protocol|lookup_result': [],
    'windows|event|network|start|connection_accepted': ['ipv4_connection_accepted', 'ipv6_connection_accepted'],
    'windows|event|network|start|connection_attempted': ['ipv4_connection_attempted', 'ipv6_connection_attempted', 'ipv4_reconnect_attempted', 'ipv6_reconnect_attempted'],
    'windows|event|process|end|end': [],
    'windows|event|process|info|-': [],
    'windows|event|process|start|start': [],
    'windows|event|registry|access|query': [],
    'windows|event|registry|change|modification': []
}



mapping = {}

class parser(object):
    def __init__(self, lines):
        self.all_ = []
        self.cur = {}
        self.lines = lines
        self.index = 0

    def parse(self):
        while self.has_more_data():
            self.parse_new_index()


        return self.all_

    def step(self):
        self.index += 1
        return self

    def has_more_data(self) -> bool:
        return self.index < len(self.lines)

    def next_line(self, bSkipBlanks = True) -> str:
        line = ""

        if self.has_more_data():
            line = self.lines[self.index]
            self.step()

        if not bSkipBlanks:
            return line

        while len(line) == 0 and self.has_more_data():
            line = self.lines[self.index]
            self.step()

        return line

    def parse_new_index(self):
        line = self.next_line()

        if not self.has_more_data():
            return

        assert line.startswith("Current index:"), f"line starts with {line}"
        self.cur = {"fields": [], "filters": []}
        parts = line.split(".")
        name = parts[-1].split("-")[0]
        self.cur["name"] = name


        # read the filters
        self.parse_filters()

        line = self.next_line()

        assert line.startswith("Field Listing:"), f"wrong field starting ({line})"
        line = self.next_line()
        assert line.startswith("**********"), f"line doesn't start with stars ({line})"

        # parse the field listing
        for _ in range(len(self.cur["filters"])):
            self.parse_fields()

        self.all_.append(self.cur)

    def parse_filters(self):
        line = self.next_line()

        if not self.has_more_data():
            return

        # starts with the filter
        assert line.startswith("host.os.type"), f"line doesn't start with filter ({line})"
        line = self.next_line()
        assert line.startswith("**********"), f"line doesn't start with stars ({line})"

        self.cur["filters"] = []
        while True:
            line = self.next_line(False)
            if len(line) == 0:
                break
            self.cur["filters"].append(line)

    def parse_fields(self):
        line = self.next_line()

        if len(line) == 0:
            return

        # this one should start with the filter
        assert line in self.cur["filters"], f"couldn't find the filter ({line})"
        fields = {"filter": line, "fields": []}

        while True:
            line = self.next_line(False)
            if len(line) == 0:
                break
            fields["fields"].append(line)
        self.cur["fields"].append(fields)

def get_json(input):
    with open(input) as f:
        # the new way
        #obj = json.load(f)
        # return obj

        # the old way
        data = f.read()
    obj = []
    cur = {}

    lines = list(map(lambda x: x.strip(), data.splitlines()))

    d = parser(lines).parse()
    return d

def get_fields_file(event_type : str) -> str:
    # go through custom_documentation/package/endpoint/data_stream/{event_types}
    here = os.path.dirname(os.path.abspath(__file__))

    cur = os.path.dirname(here)
    last = here
    there = ""
    while True:
        if cur == last:
            break
        if os.path.isdir(os.path.join(cur, "custom_documentation")):
            there = cur
            break

        last = cur
        cur = os.path.dirname(cur)

    data_streams = os.path.join(there, "custom_documentation", "package", "endpoint",
                                "data_stream")

    result = os.path.join(data_streams, event_type, "fields", "fields.yml")

    return result

def load_field_file(path : str) -> dict:
    assert os.path.exists(path), f"field file does not exist at path {path}"

    import yaml
    with open(path) as f:
        obj = load(f, Loader=Loader)


    # Given a fields.yml file and a dump of the output
    # We want to go through each field in each search result and update the fields.yml object
    # with tailored filtration
    return obj

def find_and_update_field_with_os_and_event(field_array, field, os_, event):
    for f in field_array:
        if f["ecs"] == field:
            if os_ not in f:
                f[os_] = []
            f[os_].append(event)
            break
    else:
        print(f"could not find {field}")

def main(args):

    obj = get_json(args.input)

    with open(f"{args.input}.json", "w") as f:
        json.dump(obj, f, indent=4)

    # loop through the search terms in the file
    for k in obj:
        data_stream = k["name"]

        # find the actual filter yaml file and read it in
        path = get_fields_file(data_stream)
        fields = load_field_file(path)

        # loop through the filters in the aggregation
        for field_item in k["fields"]:
            f = field_item["filter"]

            # the filter is a pipe-delimited combination of the search terms
            parts = f.split("|")
            os_ = parts[0]

            # this is the number of events that correspond to this search mapping
            events = field_mapping.get(f, [])

            # if there is no mapping for this, skip this one
            if len(events) == 0:
                continue

            for event_name in events:
                print(f"{os_} for {event_name} -- {data_stream} (updating {len(field_item['fields'])} fields)")

                # for each field_map, add to the list of os-specific event names
                for field in field_item["fields"]:
                    find_and_update_field_with_os_and_event(fields["fields"], field, os_, event_name)

        with open(path, "w") as f:
            dump(fields, f, Dumper=Dumper)

    return 0

if __name__ == "__main__":

    cmdline = argparse.ArgumentParser()
    cmdline.add_argument("input", help="the output from running Michelle's script")

    args = cmdline.parse_args()

    sys.exit(main(args))
