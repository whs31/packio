import os
from conan import ConanFile
from conan.tools.layout import basic_layout
from conan.tools.build import check_min_cppstd
from conan.tools.files import copy


class PackioConan(ConanFile):
    name = "packio"
    version = "2.5.0"
    license = "MPL-2.0"
    author = "Quentin Chateau <quentin.chateau@gmail.com>"
    url = "https://github.com/qchateau/packio"
    package_type = "header-library"
    description = "Asynchrnous msgpack-RPC and JSON-RPC server and client"
    topics = (
        "rpc",
        "async",
        "msgpack",
        "json",
        "msgpack-rpc",
        "json-rpc",
        "cpp17",
        "cpp20",
        "coroutine",
    )
    exports_sources = "include/*"
    no_copy_source = True

    @property
    def _min_cppstd(self):
        return "17"

    def layout(self):
        basic_layout(self)

    def validate(self):
        if self.settings.get_safe("compiler.cppstd"):
            check_min_cppstd(self, self._min_cppstd)

    def configure(self):
        self.options["msgpack-cxx"].use_boost = False

    def requirements(self):
        self.requires(
            "msgpack-cxx/4.1.3", transitive_libs=True, transitive_headers=True
        )
        self.requires(
            "nlohmann_json/3.11.3", transitive_libs=True, transitive_headers=True
        )
        self.requires("asio/[>=1.32.0]", transitive_libs=True, transitive_headers=True)

    def package(self):
        copy(
            self,
            pattern="*.h",
            dst=os.path.join(self.package_folder, "include"),
            src=os.path.join(self.source_folder, "include"),
        )

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "packio")
        self.cpp_info.set_property("cmake_target_name", "packio::packio")
        self.cpp_info.requires = [
            "msgpack-cxx::msgpack-cxx",
            "asio::asio",
            "nlohmann_json::nlohmann_json",
        ]
        self.cpp_info.defines.append("PACKIO_STANDALONE_ASIO=1")
        self.cpp_info.defines.append("PACKIO_HAS_MSGPACK=1")
        self.cpp_info.defines.append("PACKIO_HAS_NLOHMANN_JSON=1")
        self.cpp_info.defines.append("PACKIO_HAS_BOOST_JSON=0")
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []
