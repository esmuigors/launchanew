# launchanew
Set of tools for managing Gaussian calculations

USAGE REQUIREMENTS:

0. (presumably) ALL scripts in the branch are required at some point
1. bash; perl; sed; awk; if You want to use problem solver, then also python. This was tested on cluster with quite ancient versions of them (bash from 3.00.15 to 4.1.2; perl from 5.8.5 to 5.10.1; sed from 4.1.2 to 4.2.1; awk from 3.1.3 to 3.1.7), so hopefully Yours will not be too old...
2. input files MUST have title section constructed in the following MANNER (not absolutely with these meanings, see line 11):
	::: input_geometry_filename* output_geometry_filename* job_group_name** job_processing_sub_name multistep_job_name** job_step_in_multistep_job***

\* should match if not optimization

** we use automated extraction of job results and storing in database in the form of spreadsheet files; hence, job_group_name is the name of a sheet inside such a file (one file for each compound); multistep_job_name is the name of compound job -- it is useful to group Your jobs in the batch file; for instance, Ionization job (that is, by ΔSCF method) consists of three steps (neutral molecule, cation, anion), with multistep_job_name=Ionization and job_step_in_multistep_job=(1; 2; 3); ExcitedStateAbsorption will have the 1st step – single point with storing the 'slow' component of the reaction field and the 2nd step – the TD calculation itself.

For launchanew to work properly, You only need to set multistep_job_name and job_step_in_multistep_job for each job title section -- why this is needed can be seen in description for options -c and -d. For example, You can use such title section:

	::: a b c d e 1
	
Notice, however, that the first step of a geometry optimization is recognized by matching 'GeometryOptimization 1', but You can modify the script to match Your names. We actually advice You to use such a naming system -- it is really convenient to use for large batches of computations.

Sometimes there is need for jobs that are not going to be archived (not like it is defined by Gaussian, as any job with IOps is NOT archived by default). For example, fragmented or other sophisticated guesses, or jobs froducing natural orbitals, etc. We are used to mark such jobs by setting their geometries to 0000_000 0000_000 (see description of -z keyword).

*** an integer from 1 to 9 (can You imagine a job with 10 steps? I never had one.)

3. You must add to Your ~/.bashrc or ~/.bash_profile the following:

	 GAUSS_SPRSCRDIR=/path/to/additional/scratch/directory/other/than/one/set/in/GAUSS_SCRDIR/if/it/is/present
	 
	 GAUSS_LNCHDIR=/path/to/directory/containing/input/output/and/checkpoint/files
	 export $GAUSS_SPRSCRDIR $GAUSS_LNCHDIR
	 
4. (optional) lutil commands marked as Gaussian comments (starting with !lutil in an input file). We use these for things like splitting large batch jobs so that output files are easier to be proceeded (!lutil echo 'Splitting..'), or producing formatted checkpoint files right during  the batch job (!lutil formchk chk_name.chk). As You can see, everything after the keyword !lutil is just executed as a bash command. When an !lutil line is encountered, the input file is split into two parts, named as /path/to/input/file_U1.gjf, /path/to/input/file_U2.gjf, and so on. If You don't use them, it is OK for the script to work properly.


USAGE: 

Usage: launchanew\[.NNN] \[OPTIONS] /path/to/inputfile.gjf \[/path/to/outputfile.out] \[&> /path/to/logfile.logg] &

Script is intended to restart failed jobs and launch additional utilities. Every failure is reported to stdout and to ~/CalcLog.logg.$HOSTNAME file. Failed job inputs are copied to file /path/to/inputfile_failed.gjf. At the end all .out and .fchk files are compressed to /path/to/inputfile.tgz and to /path/to/inputfile_fchks.tgz, respectively. If the output file contains no 'Normal termination' lines, by default IT WILL BE DELETED after launchanew finishes; this can be overridden by specifying -u option.

At the end congratulations are printed.

If the name of input file is not specified, that of input file is used, replacing '.gjf' with '.out'.


OPTIONS:

Whether to delete scratch files in $GAUSS_SCRDIR directory or not to do that:

   * no option: do this after every misrun of Gaussian
   
   * -r or --remove:	do this once in the beginning
   
   * -a or --noalltimeneat:	SUPPRESS DOING SO after every misrun of Gaussian.
   
Behaviour regarding jobs using checkpoint files that were modified by failed jobs:

  *  no option: all jobs until the end of compound job will be omitted. A compound job contains multiple steps which are neede to obtain complete results.
   
  * -c or  --ccheck:	job using chk from job just failed will be omitted
   
  * -d or --nodscheck:	script will NOT remove even steps remaining in the failed multistep job that used the .CHK   
   
-o or --useoldchk:	continue from the previous CHK file without foolproofing. By default, launchanew will abort if any of .chk files mentioned in the input are found in the present directory.

-s or --notrysolve:	script will NOT try to solve SCF convergence or integration, or Opt=CalcAll or Polar problems, e.g., switch off FMM when neccessary.

-w or --norwfmod:	do not modify the size or RWF files according to available disk on the node (You may have done it before using different parameters for determination of optimal RWF size)

-p or --noprocmod:	do not modify the available memory and number of CPU cores (You may have done it before using different parameters for determination of optimal memory size)

-z or --okzero:	do NOT remove after the calculation all those files title section of which starts with '::: 0000_000 0000_000'; these files were used to generate .FCHK with relevant data (NO, NTO, etc.)

-u or --okstupid:	suppress deletion of the output file if it contains no 'Normal termination's or a functional lacked abilities for a compound job

-k or --nodalek:	allows to make job immune to the dalek (a script that is run constantly and every 60 minutes checks for hung-up script over the whole cluster).

-m or --monram:	request monitoring RAM usage every 5 minutes, with writing to file ~/MemLog.$(uname -n).logg

-q or --requirements:	display requirements for this script

-h or --help:	display this help.


Options CAN be specified in bulk (e. g., launchanew -crom input.file).
