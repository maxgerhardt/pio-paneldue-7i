Import("env")
from os.path import join

pio_platform = env.PioPlatform()
atmel_cmsis_dir = pio_platform.get_package_dir("framework-cmsis-atmel")
cmsis_dir = pio_platform.get_package_dir("framework-cmsis")

env.Append(
  CPPPATH=[
    join(atmel_cmsis_dir, "CMSIS", "Device", "ATMEL"),
    join(atmel_cmsis_dir, "CMSIS", "Device", "ATMEL", "sam4s", "include"), #convenience for our chip
    join(cmsis_dir, "CMSIS", "Core", "Include"),
  ],
  LINKFLAGS=["--specs=nosys.specs", "--specs=nano.specs"]
)

# link against libmath (implicit at the end), libc, libgcc
env.Replace(
   LIBS=["c", "gcc", "m", "stdc++"]
)

# fix linkerscript
# also SRAM linker script available
env.Append(LIBPATH=[join(atmel_cmsis_dir, "CMSIS", "Device", "ATMEL", "sam4s", "source", "as_gcc")])
env.Replace(LDSCRIPT_PATH ="sam4s4b_flash.ld")

# build startup file
# for that we additionally need to define macros that tell it what peripherals we have.. sadly not implied automatically
env.Append(
  CPPDEFINES= [
     "_SAM4S_USART1_INSTANCE_",
     "_SAM4S_HSMCI_INSTANCE_",
     "_SAM4S_DACC_INSTANCE_"
 ]
)

# build system file (starts up clocks) and startup file (contains interrupt vector table)
system_file_dir = join(atmel_cmsis_dir, "CMSIS", "Device", "ATMEL", "sam4s", "source")
system_file_dir_filter = "-<*> +<system_sam4s.c> +<as_gcc/startup_sam4s.c>"
env.BuildSources(join("$BUILD_DIR", "FrameworkCMSIS"), system_file_dir, src_filter=system_file_dir_filter)
