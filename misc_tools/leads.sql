DROP VIEW IF EXISTS leads;
create view leads as
select distinct 
	public.data_permitdataotherprofessionals."RECORD_NUMBER"
	,"PROFESSIONALS"
	,substring("PROFESSIONALS", ' [^ ]{1,50}@[^\n]{1,55}') as email
	,substring(substring("PROFESSIONALS", '\nPhone[^@]{1,10}[0-9]{3}-{0,1}[0-9]{3}-{0,1}[0-9]{4}'), '[0-9]{3}-{0,1}[0-9]{3}-{0,1}[0-9]{4}') as phone
	,substring(substring("PROFESSIONALS", 'Mobile[^@]{1,10}[0-9]{3}-{0,1}[0-9]{3}-{0,1}[0-9]{4}'), '[0-9]{3}-{0,1}[0-9]{3}-{0,1}[0-9]{4}') as mobile
	,substring("PROFESSIONALS", '\n[^@]{1,50}\n') as "BUSINESS_NAME"
	,"CONSTRUCTION_TYPE"
	,"PERMIT_TYPE"
	,"SUBPERMIT_TYPE" 
	,"CONSTRUCTION_VALUE"
	,"AC_UNIT_MAKE"
	,"AC_UNIT_MODEL"
	,"RES_OR_COMM"
	,"DATE"
	
FROM public.data_permitdataotherprofessionals
left join public.data_permitdataotherdetails
on public.data_permitdataotherprofessionals."RECORD_NUMBER" = public.data_permitdataotherdetails."RECORD_NUMBER"

left join public.data_permitdata
on public.data_permitdataotherprofessionals."RECORD_NUMBER" = public.data_permitdata."RECORD_NUMBER"

where "PROFESSIONALS" like '%@%'
and "CONSTRUCTION_VALUE" is not null
;

-- SELECT id, "RECORD_NUMBER", "JOB_VALUE", "CONSTRUCTION_TYPE", "PERMIT_TYPE", "SUBPERMIT_TYPE", "CONSTRUCTION_VALUE", "WORK_AREA", "PARCEL_NUMBER", "AC_UNIT_MAKE", "AC_UNIT_MODEL", "ADDITIONAL_COSTS", "EXISTING_STRUCTURE_ADDITIONS", "NUM_ROOF_AC_UNITS", "RES_OR_COMM", "LOAD_DATE_TIME"
-- FROM public.data_permitdataotherdetails;

-- SELECT id, "COUNTY", "DATE", "RECORD_TYPE", "RECORD_NUMBER", "STATUS", "ACTION", "ADDRESS", "PROJECT_NAME", "EXPIRATION_DATE", "DESCRIPTION", "LOAD_DATE_TIME", "LICENSE_TYPE"
-- FROM public.data_permitdata;


