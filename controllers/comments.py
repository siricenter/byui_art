
##### Comment post forms ######################
# TODO: Comments might need to be separated from the form so that they can be seen even if the user is not logged in
@auth.requires_login()
def item_post():
	itemId=request.args[0]
	form=SQLFORM(db.t_item_comment, fields=['f_comment'])
	form.vars.f_status = 'Pending'
	form.vars.f_item_id = itemId
	if form.process().accepted:
		response.flash = 'Comment awaiting moderation'
	elif form.errors:
		response.flash = 'Comment form has had an error. Please try again.'
	return dict(form=form)

@auth.requires_login()
def coll_post():
	collectionId = request.args[0]
	form=SQLFORM(db.t_coll_comment, fields=['f_comment'])
	form.element('textarea')['_rows'] = 6
	form.element('textarea')['_cols'] = 70
	form.vars.f_status = 'Pending'
	form.vars.f_collection_id = collectionId
	if form.process().accepted:
		response.flash = 'Comment awaiting moderation'
	elif form.errors:
		response.flash = 'Comment form has had an error. Please try again.'
	return dict(form=form)

###############################################
##### Individual comments dashboard calls #####

def item_load():
	db.t_item_comment.f_status.writable = False
	i_form = SQLFORM.grid(db.t_item_comment.created_by == auth.user_id,searchable=False,
				create=False,formname='item_grid',onupdate=set_status_i)
	return dict(i_form=i_form)

def coll_load():
	db.t_coll_comment.f_status.writable = False
	c_form = SQLFORM.grid(db.t_coll_comment.created_by == auth.user_id,searchable=False,
				create=False,formname='coll_grid',onupdate=set_status_c)
	return dict(c_form=c_form)

###############################################
##### Comments moderation page calls ##########

def item_comm_mang():
	subset = request.vars['subset']
	db.t_item_comment.f_comment.writable = False
	db.t_item_comment.f_item_id.writable = False
	if subset == 'all':
		i_form = SQLFORM.grid(db.t_item_comment,create=False,deletable=False,
			orderby=~db.t_item_comment.f_status,formname='item_grid',paginate=10,csv=False,
			fields=(db.t_item_comment.f_comment,
					db.t_item_comment.f_item_id,
					db.t_item_comment.f_status))
	else:
		i_form = SQLFORM.grid(db.t_item_comment.f_status == 'Pending',create=False,deletable=False,
			orderby=~db.t_item_comment.f_status,formname='item_grid',paginate=10,csv=False,
			fields=(db.t_item_comment.f_comment,
					db.t_item_comment.f_item_id,
					db.t_item_comment.f_status))
	return dict(i_form=i_form)

def coll_comm_mang():
	subset = request.vars['subset']
	db.t_coll_comment.f_comment.writable = False
	db.t_coll_comment.f_collection_id.writable = False
	if subset == 'all':
		c_form = SQLFORM.grid(db.t_coll_comment,create=False,deletable=False,
			orderby=~db.t_coll_comment.f_status,formname='coll_grid',paginate=10,csv=False,
			fields=(db.t_coll_comment.f_comment,
					db.t_coll_comment.f_collection_id,
					db.t_coll_comment.f_status))
	else:
		c_form = SQLFORM.grid(db.t_coll_comment.f_status == 'Pending',create=False,deletable=False,
			orderby=~db.t_coll_comment.f_status,formname='coll_grid',paginate=10,csv=False,
			fields=(db.t_coll_comment.f_comment,
					db.t_coll_comment.f_collection_id,
					db.t_coll_comment.f_status))
	return dict(c_form=c_form)

###############################################

def set_status_i(form):
	comm_id = form.vars.id
	db(db.t_item_comment.id == comm_id).update(f_status='Pending')

def set_status_c(form):
	comm_id = form.vars.id
	db(db.t_coll_comment.id == comm_id).update(f_status='Pending')