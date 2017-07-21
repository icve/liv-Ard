- web ui shows current status of devides and settings
- auto deploy script
- get coverage
- continuous integration
- write perf test
+ investigate why 962 byte per second is the maximum transfer rate and seek for improvement
    note1:
        dry run(skip writing to serial) 'transfers' up to 18400 - 18600 bps cpu goes to 100% 
        specs: update_intv=0 
        module_loaded, sev clock, rainfall(max_height=6, max_speed=1000, min_speed=1000), motion_sensor, lcd slide

- implement curpos update on leftToRight cmd
- write test!
- new dPrint case:
	- if the gap between sensor and cloestest cluster is less than the overhead, directly print string instead of seting cursor to 1 diff char location 
