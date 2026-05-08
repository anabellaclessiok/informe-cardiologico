from supabase import create_client
import streamlit as st

def get_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def guardar_informe(datos):
    try:
        supabase = get_client()
        informe = {
            "paciente":        datos.get("paciente", ""),
            "edad":            datos.get("edad", ""),
            "fecha":           datos.get("fecha", ""),
            "obra_social":     datos.get("obra_social", ""),
            "medico_solicita": datos.get("medico_solicita", ""),
            "ddvi":            datos.get("ddvi", ""),
            "dsvi":            datos.get("dsvi", ""),
            "fa":              datos.get("fa", ""),
            "fe":              datos.get("fe", ""),
            "sep":             datos.get("sep", ""),
            "pp":              datos.get("pp", ""),
            "vd":              datos.get("vd", ""),
            "ao":              datos.get("ao", ""),
            "ai":              datos.get("ai", ""),
            "ai_area":         datos.get("ai_area", ""),
            "ai_vol":          datos.get("ai_vol", ""),
            "imvi":            datos.get("imvi", ""),
            "vel_ao":          datos.get("vel_ao", ""),
            "grad_ao":         datos.get("grad_ao", ""),
            "vel_pul":         datos.get("vel_pul", ""),
            "grad_pul":        datos.get("grad_pul", ""),
            "onda_e":          datos.get("onda_e", ""),
            "onda_a":          datos.get("onda_a", ""),
            "psap":            datos.get("psap", ""),
            "hallazgos":       datos.get("hallazgos", ""),
            "doppler":         datos.get("doppler", ""),
            "conclusion":      datos.get("conclusion", ""),
        }
        supabase.table("informes").insert(informe).execute()
        return True
    except Exception as e:
        st.error(f"Error al guardar: {e}")
        return False

def buscar_informes(nombre):
    try:
        supabase = get_client()
        resultado = supabase.table("informes")\
            .select("*")\
            .ilike("paciente", f"%{nombre}%")\
            .order("creado_en", desc=True)\
            .execute()
        return resultado.data
    except Exception as e:
        st.error(f"Error al buscar: {e}")
        return []

def obtener_todos():
    try:
        supabase = get_client()
        resultado = supabase.table("informes")\
            .select("id, paciente, fecha, creado_en")\
            .order("creado_en", desc=True)\
            .limit(50)\
            .execute()
        return resultado.data
    except Exception as e:
        st.error(f"Error al obtener informes: {e}")
        return []

def obtener_informe_por_id(id):
    try:
        supabase = get_client()
        resultado = supabase.table("informes")\
            .select("*")\
            .eq("id", id)\
            .execute()
        return resultado.data[0] if resultado.data else None
    except Exception as e:
        st.error(f"Error al obtener informe: {e}")
        return None