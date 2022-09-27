# Publishing Protocols

**Coincidence Tier**

* ``p_value`` and ``neutrino_time`` need to be passed.
    * ``p_val`` must be a ``float``.
    * ``neutrino_time`` must be a ``string`` with ISO format: ``"%Y-%m-%dT%H:%M:%S.%f"``

**Significance Tier**

* ``p_values`` needs to be passed.
    * ``p_values`` must be a ``list (float)``.

**Timing Tier**

* ``p_value`` and ``timing_series`` need to be passed.
    * ``p_val`` must be a ``float``.
    * ``timing_series`` must be a ``list (string)``, ISO format: ``"%Y-%m-%dT%H:%M:%S.%f"``

**Retraction**

* ``n_retract_latest`` and ``which`` need to be passed.
    * ``n_retract_latest`` must be a ``int (and >0 )``. You can also pass it as a ``'ALL'``.
    * ``which_tier`` must be a ``which_tier``

**Pre-SN Timing Tier**

* ``is_pre_sn`` and ``timing_series`` need to be passed.
    * ``is_pre_sn`` must be a ``bool``.
    * ``timing_series`` must be a ``list (string)``, ISO format: ``"%Y-%m-%dT%H:%M:%S.%f"``

Notice that your message can contain fields that corresponds to several tiers e.g. if you have ``p_value``, ``neutrino_time``, and ``p_values`` we submit two separate messages to _Coincidence_ and _Significance_ tiers by selecting the relevant fields from your input.
