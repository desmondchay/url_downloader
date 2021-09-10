# Defining Requirements

- Need to get file size first with HEAD
- Need to account for system size,
- Need to handle case when download fail (to not have the partially downloaded file stored)
- Need to support ftp, http, https
- Need to dockerize 
- May need to try making it concurrent
- Need to stream for files that cannot fit in memory