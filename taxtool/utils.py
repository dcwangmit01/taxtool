import subprocess
import re
import yaml


class Utils(object):
    @staticmethod
    def write_string_to_file(s, file):
        with open(file, "w") as f:
            f.write(s)
            f.close()

    @staticmethod
    def read_string_from_file(file):
        data = ""
        with open(file, "r") as f:
            data = f.read()
            f.close()
        return data

    @staticmethod
    def yaml_dict_write_to_file(dict, file):
        s = yaml.safe_dump(dict, default_flow_style=False)
        return Util.write_string_to_file(s, file)

    @staticmethod
    def yaml_dict_read_from_file(file):
        s = Util.read_string_from_file(file)
        d = yaml.load(s)
        return d

    @staticmethod
    def exec_command(command):

        try:
            #print("executing command[{}]".format(command))
            res = subprocess.check_output(command, shell=True)

            try:  # pretty print json if the output happens to be
                res = json.dumps(json.loads(res), indent=2, sort_keys=True)
            except Exception as e:
                pass

            #print("executing command[{}] returned[{}]".format(command, res))
            return (res, None)
        except Exception as e:
            return ('<Error>', str(e))

    @staticmethod
    def pad_str(pad, num, s):
        return re.sub("^", (pad * num), s, 0, re.MULTILINE)

    @staticmethod
    def sort_str(s):
        t = s.split("\n")
        t.sort()
        return "\n".join(t)
