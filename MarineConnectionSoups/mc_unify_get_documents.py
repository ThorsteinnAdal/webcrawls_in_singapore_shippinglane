__author__ = 'thorsteinn'


def mc_unify_get_documents(folder, file_base, **kwargs):
    from glob import glob
    import os
    from db_to_file_helpers.jsonDicts_to_file import file_to_db, db_to_file

    output_file = kwargs.pop('output_file', 'mc_db_master.txt')
    foot = os.path.dirname(folder)
    ff = os.path.join(foot, file_base)
    file_glob = glob(ff + '*')
    if len(file_glob) is 0:
        print "No files with the name-base {file_base!r} were found under the root: {foot!r}\n" \
              "Check the input file_base and try again".format(
            file_base=file_base,
            foot=foot
        )
        return False


    db = {}
    for one_file in file_glob:
        print one_file
        small_db = file_to_db(one_file)
        db.update(small_db)

    db_to_file(db, os.path.join(foot, output_file))
    print "Collected {number} of records into the output file: {output_file}".format(number=len(db), output_file=os.path.join(foot, 'dnv_db_master.txt'))


if __name__ == "__main__":
    mc_unify_get_documents('./all_get_db_masters/','mc_db_')