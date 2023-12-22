Ctrl-C does not give the control back to the user

https://github.com/encode/uvicorn/issues/1010

Interesting : 

debian : 

    $ stty -a
    speed 38400 baud; rows 43; columns 182; line = 0;
    intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = <undef>; eol2 = <undef>; swtch = <undef>; start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V;
    discard = ^O; min = 1; time = 0;
    -parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts
    -ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc ixany imaxbel iutf8
    opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
    isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho -extproc


macos : 
    
    $ stty -e
    speed 38400 baud; 29 rows; 181 columns;
    lflags: icanon isig iexten echo echoe echok echoke -echonl echoctl
        -echoprt -altwerase -noflsh -tostop -flusho pendin -nokerninfo
        -extproc
    iflags: -istrip icrnl -inlcr -igncr ixon -ixoff ixany imaxbel iutf8
        -ignbrk brkint -inpck -ignpar -parmrk
    oflags: opost onlcr -oxtabs -onocr -onlret
    cflags: cread cs8 -parenb -parodd hupcl -clocal -cstopb -crtscts -dsrflow
        -dtrflow -mdmbuf
    discard dsusp   eof     eol     eol2    erase   intr    kill    lnext
    ^O      ^Y      ^D      <undef> <undef> ^?      ^C      ^U      ^V
    min     quit    reprint start   status  stop    susp    time    werase
    1       ^\      ^R      ^Q      ^T      ^S      ^Z      0       ^W

debian :
    
    $ showkey -a
    
    Press any keys - Ctrl-D will terminate this program
    
    ^U 	 21 0025 0x15
    ^C 	  3 0003 0x03
    ^O 	 15 0017 0x0f

In bash, Ctrl-4 and Ctrl-$ sends Ctrl-\ 

https://unix.stackexchange.com/questions/226327/what-does-ctrl4-and-ctrl-do-in-bash
    
    $ showkey -a
    
    Press any keys - Ctrl-D will terminate this program
    
    ^\ 	 28 0034 0x1c

