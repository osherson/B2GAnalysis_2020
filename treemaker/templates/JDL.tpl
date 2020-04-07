cd /cms/universe = vanilla
Requirements = (Arch == "X86_64")
+RUQueue = "cms"
+AccountingGroup = "group_rutgers.#USER#"
Executable = #EXEC#.sh
should_transfer_files = NO
Output = #PATH#/#EXEC#_$(cluster)_$(process).stdout
Error = #PATH#/#EXEC#_$(cluster)_$(process).stderr
Log = #PATH#/#EXEC#_$(cluster)_$(process).condor
Arguments = $(cluster) $(process)
Queue 1
