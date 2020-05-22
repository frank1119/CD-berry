# [CD-berry](https://github.com/frank1119/CD-berry)
Solid State CD-ROM emulation with a Raspberry Pi Zero

### Current status
This project is now complete. Writing the Wiki, which is an important part, has been completed. The source files have been uploaded

# Rationale
When upgrading BIOS firmware on servers (e.g. Dell R<number> servers) sometimes the only way to perform these is using a CD-ROM. Often a bootable USB-stick is not possible, because the OS applied by the software (e.g. Dell Repository Manager) creating firmware upgrade deployments expects to mount a CD-ROM. A USB-stick just won't work.
To solve this a normal CD could be burned, but well, writable CD-ROMs are not that common any more and also CD-burners are becoming more and more an exception.
My long-term solution is a Raspberry Pi Zero emulating a USB CD-ROM player.
  
# Content
In this project are some sources to make the solution viable and, very important, an extensive [Wiki](https://github.com/frank1119/CD-berry/wiki) how to set up the Raspberry Pi Zero

# (Not enough) support for DVDs larger than 2 GB
The patch for DVDs larger than about 2 GB seems to be flawed. Using Windows it seems to work well enough. Linux, however, does not read the larger DVDs, even when patched. I've implemented a new patch, but that patch is not as easy to apply as the old 'patch' and differs depending on the linux kernel sources version
