================================
Varnish plugin for Ganglia Gmond
================================

This is a Python plugin for gmond_ that collects statistics from Varnish_.

Installation
============

You will need to have Ganglia's gmond installed, and you will need the
optional Python module support. Under RHEL5/CentOS, the necessary packages
are:

- ganglia-gmond-3.1.7-1
- ganglia-gmond-modules-python-3.1.7-1

To install everything by hand::

  # make install

You may also build an RPM from this package for installation onto
RedHat-ish systems.

Configuration
=============

The makefile install a sample configuration file as
``varnishstats.pyconf.sample``.  This configures a subset of the metrics
available from the module.  To see a complete list of available metrics,
run::

  /usr/lib/ganglia/python_modules/varnishstats.py -M

Note that varnish must be running in order for this to work.  The module
also supports two configuration parameters:

- RefreshRate -- how often to refresh the metrics.  This is the basic
  period for which deltas are calculated.  Default: 60 seconds.

- VarnishstatPath -- Path to ``varnishstat`` executable.  This defaults to
  simply ``varnishstat``, but if it can't be found in ``$PATH`` you can
  provide an explicit path here.

Available metrics
=================

Every value produced by the ``varnishstat`` program is exposed through this
module.  Additionally,  for each metric, a second metric with the ``_delta``
suffix is generated that tracks the change in value between each update.
In many cases, the ``_delta`` metric is probably what you want.

This is the complete list of metrics available when running this module in
conjunction with varnish 2.1.4:

- client_conn
- client_conn_delta
- client_drop
- client_drop_delta
- client_req
- client_req_delta
- cache_hit
- cache_hit_delta
- cache_hitpass
- cache_hitpass_delta
- cache_miss
- cache_miss_delta
- backend_conn
- backend_conn_delta
- backend_unhealthy
- backend_unhealthy_delta
- backend_busy
- backend_busy_delta
- backend_fail
- backend_fail_delta
- backend_reuse
- backend_reuse_delta
- backend_toolate
- backend_toolate_delta
- backend_recycle
- backend_recycle_delta
- backend_unused
- backend_unused_delta
- fetch_head
- fetch_head_delta
- fetch_length
- fetch_length_delta
- fetch_chunked
- fetch_chunked_delta
- fetch_eof
- fetch_eof_delta
- fetch_bad
- fetch_bad_delta
- fetch_close
- fetch_close_delta
- fetch_oldhttp
- fetch_oldhttp_delta
- fetch_zero
- fetch_zero_delta
- fetch_failed
- fetch_failed_delta
- n_sess_mem
- n_sess_mem_delta
- n_sess
- n_sess_delta
- n_object
- n_object_delta
- n_vampireobject
- n_vampireobject_delta
- n_objectcore
- n_objectcore_delta
- n_objecthead
- n_objecthead_delta
- n_smf
- n_smf_delta
- n_smf_frag
- n_smf_frag_delta
- n_smf_large
- n_smf_large_delta
- n_vbe_conn
- n_vbe_conn_delta
- n_wrk
- n_wrk_delta
- n_wrk_create
- n_wrk_create_delta
- n_wrk_failed
- n_wrk_failed_delta
- n_wrk_max
- n_wrk_max_delta
- n_wrk_queue
- n_wrk_queue_delta
- n_wrk_overflow
- n_wrk_overflow_delta
- n_wrk_drop
- n_wrk_drop_delta
- n_backend
- n_backend_delta
- n_expired
- n_expired_delta
- n_lru_nuked
- n_lru_nuked_delta
- n_lru_saved
- n_lru_saved_delta
- n_lru_moved
- n_lru_moved_delta
- n_deathrow
- n_deathrow_delta
- losthdr
- losthdr_delta
- n_objsendfile
- n_objsendfile_delta
- n_objwrite
- n_objwrite_delta
- n_objoverflow
- n_objoverflow_delta
- s_sess
- s_sess_delta
- s_req
- s_req_delta
- s_pipe
- s_pipe_delta
- s_pass
- s_pass_delta
- s_fetch
- s_fetch_delta
- s_hdrbytes
- s_hdrbytes_delta
- s_bodybytes
- s_bodybytes_delta
- sess_closed
- sess_closed_delta
- sess_pipeline
- sess_pipeline_delta
- sess_readahead
- sess_readahead_delta
- sess_linger
- sess_linger_delta
- sess_herd
- sess_herd_delta
- shm_records
- shm_records_delta
- shm_writes
- shm_writes_delta
- shm_flushes
- shm_flushes_delta
- shm_cont
- shm_cont_delta
- shm_cycles
- shm_cycles_delta
- sm_nreq
- sm_nreq_delta
- sm_nobj
- sm_nobj_delta
- sm_balloc
- sm_balloc_delta
- sm_bfree
- sm_bfree_delta
- sma_nreq
- sma_nreq_delta
- sma_nobj
- sma_nobj_delta
- sma_nbytes
- sma_nbytes_delta
- sma_balloc
- sma_balloc_delta
- sma_bfree
- sma_bfree_delta
- sms_nreq
- sms_nreq_delta
- sms_nobj
- sms_nobj_delta
- sms_nbytes
- sms_nbytes_delta
- sms_balloc
- sms_balloc_delta
- sms_bfree
- sms_bfree_delta
- backend_req
- backend_req_delta
- n_vcl
- n_vcl_delta
- n_vcl_avail
- n_vcl_avail_delta
- n_vcl_discard
- n_vcl_discard_delta
- n_purge
- n_purge_delta
- n_purge_add
- n_purge_add_delta
- n_purge_retire
- n_purge_retire_delta
- n_purge_obj_test
- n_purge_obj_test_delta
- n_purge_re_test
- n_purge_re_test_delta
- n_purge_dups
- n_purge_dups_delta
- hcb_nolock
- hcb_nolock_delta
- hcb_lock
- hcb_lock_delta
- hcb_insert
- hcb_insert_delta
- esi_parse
- esi_parse_delta
- esi_errors
- esi_errors_delta
- accept_fail
- accept_fail_delta
- client_drop_late
- client_drop_late_delta
- uptime
- uptime_delta
- backend_retry
- backend_retry_delta
- dir_dns_lookups
- dir_dns_lookups_delta
- dir_dns_failed
- dir_dns_failed_delta
- dir_dns_hit
- dir_dns_hit_delta
- dir_dns_cache_full
- dir_dns_cache_full_delta
- cache_hit_ratio
- cache_hit_pct

Author
======

Lars Kellogg-Stedman <lars@oddbit.com>

.. _gmond: http://ganglia.sourceforge.net/
.. _varnish: http://www.varnish-cache.org/

