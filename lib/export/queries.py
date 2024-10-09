GET_VOTERS_AFLCIO_MATCHED = """
WITH rosetta_file AS (
    SELECT
        col26_affiliate_data2 as spid,
        countyfileid,
        MAX(file_submission_date) AS file_date
    FROM
        political.aflcio_matchfiles_merged
    WHERE col26_affiliate_data2 IS NOT NULL
        AND col7_local = '{{local_number}}'
        AND regaddrstate = '{{state}}'
        AND countyname = '{{county}}'
    GROUP BY
        col26_affiliate_data2, countyfileid
    ORDER BY
        col26_affiliate_data2
)

SELECT
    voter_pipeline.*,
    rosetta_file.spid
FROM
    {{vp_schema}}.voter_pipeline
INNER JOIN
    rosetta_file ON voter_pipeline.idnumber = rosetta_file.countyfileid
"""
