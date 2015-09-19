package com.project;

import android.graphics.Bitmap;
import android.graphics.drawable.Drawable;

public class RestaurantInfo {

	protected String restName;
	protected String restDesc;
	protected Bitmap restbitMap;
	protected String restUrl;
	protected Drawable plcUrl;
	protected String restAddr;
	protected String restId;
	protected String restTiming;

	public String getRestTiming() {
		return restTiming;
	}

	public void setRestTiming(String restTiming) {
		this.restTiming = restTiming;
	}

	public String getRestId() {
		return restId;
	}

	public void setRestId(String restId) {
		this.restId = restId;
	}

	protected String getRestAddr() {
		return restAddr;
	}

	protected void setRestAddr(String restAddr) {
		this.restAddr = restAddr;
	}

	protected Drawable getPlcUrl() {
		return plcUrl;
	}

	protected void setPlcUrl(Drawable plcUrl) {
		this.plcUrl = plcUrl;
	}

	protected String getRestName() {
		return restName;
	}

	protected void setRestName(String restName) {
		this.restName = restName;
	}

	protected String getRestDesc() {
		return restDesc;
	}

	protected void setRestDesc(String restDesc) {
		this.restDesc = restDesc;
	}

	protected Bitmap getRestbitMap() {
		return restbitMap;
	}

	protected void setRestbitMap(Bitmap restbitMap) {
		this.restbitMap = restbitMap;
	}

	protected String getRestUrl() {
		return restUrl;
	}

	protected void setRestUrl(String restUrl) {
		this.restUrl = restUrl;
	}

}