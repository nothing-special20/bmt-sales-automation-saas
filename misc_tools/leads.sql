select DISTINCT
	public.data_permitdataotherprofessionals."RECORD_NUMBER"
	,"PROFESSIONALS"
	,substring("PROFESSIONALS", ' [^ ]{1,50}@[^\n]{1,15}') as email
	,substring(substring("PROFESSIONALS", '\nPhone[^@]{1,10}[0-9]{3}-{0,1}[0-9]{3}-{0,1}[0-9]{4}'), '[0-9]{3}-{0,1}[0-9]{3}-{0,1}[0-9]{4}') as phone
	,substring(substring("PROFESSIONALS", 'Mobile[^@]{1,10}[0-9]{3}-{0,1}[0-9]{3}-{0,1}[0-9]{4}'), '[0-9]{3}-{0,1}[0-9]{3}-{0,1}[0-9]{4}') as mobile	
	,"CONSTRUCTION_TYPE"
	,"PERMIT_TYPE"
	,"SUBPERMIT_TYPE" 
	,"CONSTRUCTION_VALUE"
	
	
FROM public.data_permitdataotherprofessionals
left join public.data_permitdataotherdetails
on public.data_permitdataotherprofessionals."RECORD_NUMBER" = public.data_permitdataotherdetails."RECORD_NUMBER"

where "PROFESSIONALS" like '%@%'
and "CONSTRUCTION_VALUE" is not null
;

-- SELECT id, "RECORD_NUMBER", "JOB_VALUE", "CONSTRUCTION_TYPE", "PERMIT_TYPE", "SUBPERMIT_TYPE", "CONSTRUCTION_VALUE", "WORK_AREA", "PARCEL_NUMBER", "AC_UNIT_MAKE", "AC_UNIT_MODEL", "ADDITIONAL_COSTS", "EXISTING_STRUCTURE_ADDITIONS", "NUM_ROOF_AC_UNITS", "RES_OR_COMM", "LOAD_DATE_TIME"
-- FROM public.data_permitdataotherdetails;


