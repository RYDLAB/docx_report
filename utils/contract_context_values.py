# Aliases
self = record  # res.partner.contract

partner = self.partner_id  # res.partner
seller = self.company_id

# Functions
_ = self._
get_date = self.get_date

# Parse date
months = ["",
          "января", "февраля", "марта", "апреля",
          "мая", "июня", "июля", "августа",
          "сентября", "октября", "ноября", "декабря",
          ]
date = get_date()
dd = date.day
mm = date.month
yyyy = date.year
yy = yyyy % 100
MM = months[mm]

dd = dd if dd // 10 else '0{}'.format(dd)
mm = mm if mm // 10 else '0{}'.format(mm)

# ctx keys must be decalared in this xml with id equal to "contract_field_{technical_name}"
ctx = {
    "contract_number": self.name,

    "dd": dd,
    "mm": mm,
    "MM": MM,
    "yy": yy,
    "yyyy": yyyy,

    "seller_name": seller.name_write,
    "seller_company_form": _(dict(seller._fields['company_form'].selection).get(seller.company_form)),
    "seller_representer_name": seller.representative_id.name,
    "seller_representer_name_parent": seller.representative_id.name_genitive,
    "seller_representer_name_initials": seller.representative_id.name_initials,
    "seller_representer_function": seller.representative_id.function,
    "seller_representer_function_parent": seller.representative_id.function_genitive,
    "seller_representer_document_parent": seller.representative_document,
    "seller_inn": seller.vat,
    "seller_kpp": seller.iec,
    "seller_ogrn": seller.psrn,
    "seller_business_address": seller.full_address,
    "seller_phone": seller.phone,
    "seller_whatsapp": seller.whatsapp,
    "seller_telegram": seller.telegram,
    "seller_email": seller.email,

    "partner_name": partner.name_write,
    "partner_inn": partner.vat,
    "partner_business_address": partner.full_address,
    "partner_phone": partner.phone,
    "partner_whatsapp": partner.whatsapp,
    "partner_telegram": partner.telegram,
    "partner_email": partner.email,
}

seller_bank = seller.bank_ids and seller.bank_ids[0]
if seller_bank:
    bank = seller_bank.bank_id
    bank_name = bank and bank.name or ""
    bank_city = "г. {city}".format(city=bank.city) if bank and bank.city else ""
    seller_bank_name = "{} {}".format(bank_name, bank_city).strip()

    ctx.update({
        "seller_bank": seller_bank_name,
        "seller_rs": seller_bank.acc_number,
        "seller_ks": bank.corr_account,
        "seller_bic": bank.bic,
    })

partner_bank = partner.bank_ids and partner.bank_ids[0]
if partner_bank:
    bank = partner_bank.bank_id
    bank_name = bank and bank.name or ""
    bank_city = "г. {city}".format(city=bank.city) if bank and bank.city else ""
    partner_bank_name = "{} {}".format(bank_name, bank_city).strip()

    ctx.update({
        "partner_bank": partner_bank_name,
        "partner_rs": partner_bank.acc_number,
        "partner_ks": bank.corr_account,
        "partner_bic": bank.bic,
    })

# Person
if not partner.is_company:
    ctx.update({
        "partner_representer_name": partner.name_write,
        "partner_representer_name_initials": partner.name_initials,
        "partner_representer_passport_number": partner.passport_number,
        "partner_representer_passport_date": partner.passport_date,
        "partner_representer_passport_department": partner.passport_department,
        "partner_representer_passport_department_code": partner.passport_department_code,
    })
    if not partner.name_write:
        ctx.update({
            "partner_name": partner.name,
            "partner_representer_name": partner.name,
        })
else:
    # Company
    ctx.update({
        "partner_company_form": _(dict(partner._fields['company_form'].selection).get(partner.company_form)),
        "partner_representer_name": partner.representative_id.name,
        "partner_representer_name_parent": partner.representative_id.name_genitive,
        "partner_representer_name_initials": partner.representative_id.name_initials,
        "partner_representer_function": partner.representative_id.function,
        "partner_representer_function_parent": partner.representative_id.function_genitive,
        "partner_representer_document_parent": partner.representative_document,
    })

    if partner.company_form == 'sp':
        # Sole Proprietor
        ctx.update({
            "partner_ip_number": partner.sp_register_number,
            "partner_ip_date": partner.sp_register_date,
            "partner_ogrnip": partner.psrn_sp,
            "partner_representer_passport_number": partner.representative_id.passport_number,
            "partner_representer_passport_date": partner.representative_id.passport_date,
            "partner_representer_passport_department": partner.representative_id.passport_department,
            "partner_representer_passport_department_code": partner.representative_id.passport_department_code,
        })
    if partner.company_form == 'plc':
        # Private Limited Company
        ctx.update({
            "partner_kpp": partner.iec,
            "partner_ogrn": partner.psrn,
        })

action = ctx
< / field >
< / record >

< !-- Action -->
< record
id = "action_get_annex_context"
model = "ir.actions.server" >
< field
name = "name" > Generate
Context
for Annex </ field >
< field
name = "model_id"
ref = "client_contracts.model_res_partner_contract_wizard" / >
< field
name = "binding_model_id"
ref = "client_contracts.model_res_partner_contract_wizard" / >
< field
name = "state" > code < / field >
< field
name = "code" >

# Aliases
self = record  # res.partner.contract.annex

seller = self.company_id
partner = self.partner_id

# Functions
_ = self.contract_id._
get_date = self.contract_id.get_date

# Parse date
months = ["",
          "января", "февраля", "марта", "апреля",
          "мая", "июня", "июля", "августа",
          "сентября", "октября", "ноября", "декабря",
          ]
date = get_date()
dd = date.day
mm = date.month
yyyy = date.year
yy = yyyy % 100
MM = months[mm]

dd = dd if dd // 10 else '0{}'.format(dd)
mm = mm if mm // 10 else '0{}'.format(mm)

order_date = self.order_id.date_order

# ctx keys must be decalared in this xml with id equal to "contract_field_{technical_name}"
ctx = {
    "contract_number": self.contract_id.name,

    "annex_name": self.name,
    "annex_number": self.counter,

    "order_name": self.order_id.name,
    "order_date": "{} {} {}".format(order_date.day, months[order_date.month], order_date.year),

    "design_cost": self.to_fixed(self.design_cost),
    "design_period": self.design_period,
    "design_doc_cost": self.to_fixed(self.design_doc_cost),
    "design_doc_period": self.design_doc_period,
    "delivery_address": self.delivery_address,
    "delivery_period": self.delivery_period,
    "installation_address": self.installation_address,
    "installation_cost": self.to_fixed(self.installation_cost),
    "installation_period": self.installation_period,
    "total_cost": self.to_fixed(self.total_cost),

    "payment_part_one": self.payment_part_one,
    "payment_part_two": self.payment_part_two,
    "payment_part_three": self.payment_part_three,
    "delivery_period": self.delivery_period,

    "dd": dd,
    "mm": mm,
    "MM": MM,
    "yy": yy,
    "yyyy": yyyy,

    "seller_name": seller.name_write,
    "seller_company_form": _(dict(seller._fields['company_form'].selection).get(seller.company_form)),
    "seller_representer_name": seller.representative_id.name,
    "seller_representer_name_parent": seller.representative_id.name_genitive,
    "seller_representer_name_initials": seller.representative_id.name_initials,
    "seller_representer_function": seller.representative_id.function,
    "seller_representer_function_parent": seller.representative_id.function_genitive,

    "seller_inn": seller.vat,
    "seller_kpp": seller.iec,
    "seller_ogrn": seller.psrn,
    "seller_business_address": seller.full_address,
    "seller_phone": seller.phone,
    "seller_email": seller.email,

    "partner_name": partner.name_write,
    "partner_representer_name": partner.representative_id.name,
    "partner_representer_name_initials": partner.representative_id.name_initials,
    "partner_inn": partner.vat,
    "partner_business_address": partner.full_address,
    "partner_phone": partner.phone,
    "partner_email": partner.email,
}

seller_bank = seller.bank_ids and seller.bank_ids[0]
if seller_bank:
    bank = seller_bank.bank_id
    bank_name = bank and bank.name or ""
    bank_city = "г. {city}".format(city=bank.city) if bank and bank.city else ""
    seller_bank_name = "{} {}".format(bank_name, bank_city).strip()

    ctx.update({
        "seller_bank": seller_bank_name,
        "seller_rs": seller_bank.acc_number,
        "seller_ks": bank.corr_account,
        "seller_bic": bank.bic,
    })

partner_bank = partner.bank_ids and partner.bank_ids[0]
if partner_bank:
    bank = partner_bank.bank_id
    bank_name = bank and bank.name or ""
    bank_city = "г. {city}".format(city=bank.city) if bank and bank.city else ""
    partner_bank_name = "{} {}".format(bank_name, bank_city).strip()

    ctx.update({
        "partner_bank": partner_bank_name,
        "partner_rs": partner_bank.acc_number,
        "partner_ks": bank.corr_account,
        "partner_bic": bank.bic,
    })

# Person
if not partner.is_company:
    ctx.update({
        "partner_representer_name": partner.name_write,
        "partner_representer_name_initials": partner.name_initials,
        "partner_representer_passport_number": partner.passport_number,
        "partner_representer_passport_date": partner.passport_date,
        "partner_representer_passport_department": partner.passport_department,
    })
    if not partner.name_write:
        ctx.update({
            "partner_name": partner.name,
            "partner_representer_name": partner.name,
        })
else:
    # Company
    ctx.update({
        "partner_company_form": _(dict(partner._fields['company_form'].selection).get(partner.company_form)),
        "partner_representer_name_parent": partner.representative_id.name_genitive,
        "partner_representer_document_parent": partner.representative_document,
        "partner_representer_function": partner.representative_id.function,
        "partner_representer_function_parent": partner.representative_id.function_genitive,
    })

    if partner.company_form == 'sp':
        # Sole Proprietor
        ctx.update({
            "partner_ip_number": partner.sp_register_number,
            "partner_ip_date": partner.sp_register_date,
            "partner_ogrnip": partner.psrn_sp,
            "partner_representer_passport_number": partner.representative_id.passport_number,
            "partner_representer_passport_date": partner.representative_id.passport_date,
            "partner_representer_passport_department": partner.representative_id.passport_department,
        })
    if partner.company_form == 'plc':
        # Private Limited Company
        ctx.update({
            "partner_kpp": partner.iec,
            "partner_ogrn": partner.psrn,
        })

action = ctx