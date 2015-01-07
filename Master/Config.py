import os
import yaml


class YAMLConfig(object):
    _config_values = {}

    def __init__(self, filename, default_keys={}, strict_mode=False):
        self.filename = filename
        self.default_keys = default_keys
        self.strict_mode = strict_mode
        self._load_config()

    def _load_config(self):
        if not os.path.exists(self.filename):
            self._make_default_config()
        else:
            f = open(self.filename, 'r')
            self._config_values = yaml.load(f)
            f.close()
            self._validate_config()
        print("[Config] Config %s loaded!" % self.filename)

    def _save_config(self):
        f = open(self.filename, "w")
        yaml.dump(self._config_values, f, indent=1)
        f.close()

    def _make_default_config(self):
        try:
            os.makedirs(os.path.dirname(self.filename))
        except:
            pass
        f = open(self.filename, "w")
        yaml.dump(self.default_keys, f, indent=1)
        f.close()
        print("[Config] Default config for %s created." % self.filename)
        self._load_config()

    def _validate_config(self):
        for key, value in self.default_keys.iteritems():
            if key not in self._config_values:
                self._config_values[key] = value
                print("[Config] Added new default %s for config %s" % (key, self.filename))
        if self.strict_mode:
            for key in self._config_values.keys():
                if key not in self.default_keys:
                    del self._config_values[key]
                    print("[Config] Deleted invlid key %s for config %s" % (key, self.filename))
                else:
                    if self._config_values[key] is None:
                        self._config_values[key] = self.default_keys[key]
                        print("[Config] Resetting invalid key type for %s in config %s." % (key, self.filename))
        self._save_config()

    def get_key(self, key):
        if key not in self._config_values:
            raise KeyError
        if isinstance(self._config_values[key], unicode):
            return self._config_values[key].encode('utf-8')
        else:
            return self._config_values[key]

    def set_key(self, key, value):
        self._config_values[key] = value
        self._save_config()

    def key_exists(self, key):
        if key in self._config_values:
            return True
        else:
            return False

    def __getitem__(self, item):
        return self.get_key(item)

    def __setitem__(self, key, value):
        self.set_key(key, value)